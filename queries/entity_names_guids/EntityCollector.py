"""
    This module contains the NerdGraphClient class, which is used to execute GraphQL queries against the New Relic API.
"""
import json
import logging
import os
from time import sleep
from dotenv import load_dotenv
import newrelic.agent

load_dotenv()  # Load environment variables from .env file


class EntityCollector:
    """
    This class contains the methods to get a list of entity names and GUId's for a given account. The get_entities
    method is the primary method called.
    """

    def __init__(self):
        """
        This is the constructor for the EntityCollection class.
        """

        self.api_key = os.getenv("NEW_RELIC_API_KEY")
        self.url = "https://api.newrelic.com/graphql"
        self.account_id = os.getenv("NEW_RELIC_ACCOUNT_ID")
        self.entities = []  # This will be a list of dictionaries containing entity names and GUIDs

    @newrelic.agent.background_task()
    def _build_queries(self, cursor=None):
        """
        This private function returns the query to get a list of APM entities for a given account. There are two
        queries, one with a cursor and one without. The cursor is used to get the next page of results.
        :return: The NerdGraph query and variables.
        """

        logging.info("Building query.")

        if cursor:
            logging.info("Cursor is not None. Building query with cursor.")

            # Query variables with a cursor
            query_variables = {
                "entity_search_query": f"domain = 'APM' AND accountId = '{self.account_id}'",
                "cursor": cursor
            }

            # Query with a cursor
            graphql_query = """
                query ($entity_search_query: String!, $cursor: String!) {
                  actor {
                    entitySearch(query: $entity_search_query, options: {limit: 10}) {
                      results(cursor: $cursor) {
                        nextCursor
                        entities {
                          guid
                          name
                        }
                      }
                    }
                  }
                }
                """
        else:
            logging.info("Cursor is None. Building query without cursor.")

            # Query variables without a cursor
            query_variables = {
                "entity_search_query": f"domain = 'APM' AND accountId = '{self.account_id}'"
            }

            # Query without a cursor
            graphql_query = """
                query ($entity_search_query: String!) {
                  actor {
                    entitySearch(query: $entity_search_query, options: {limit: 10}) {
                      results {
                        nextCursor
                        entities {
                          guid
                          name
                        }
                      }
                    }
                  }
                }
                """

        return graphql_query, query_variables

    @newrelic.agent.background_task()
    def get_entities(self, nerdgraph_client):
        """
        This method is the primary method called to get a list of entity names and GUIDs for a given account.
        :param nerdgraph_client: A NerdGraphClient object.
        :return: A list of dictionaries containing entity names and GUIDs.
        """

        query, variables = self._build_queries()    # Get the query and variables

        logging.info("Sending query to New Relic NerdGraph API.")
        response = nerdgraph_client.send_query(query, variables)

        next_cursor = self._process_response(response)  # Process the response and get the next cursor, if any

        while next_cursor:
            query, variables = self._build_queries(next_cursor)
            response = nerdgraph_client.send_query(query, variables)
            next_cursor = self._process_response(response)
            sleep(0.5)

        return self.entities

    @newrelic.agent.background_task()
    def _process_response(self, response):
        """
        This private function processes the response from the API request. This includes getting the next cursor,
        if any, and appending the entities to the entities list.
        :param response: The JSON response from the API request.
        :return: The next cursor, if any.
        """

        try:
            next_cursor = response["data"]["actor"]["entitySearch"]["results"]["nextCursor"]
        except KeyError:
            logging.error("KeyError: 'nextCursor' not found in response.")
            next_cursor = None

        entities = response["data"]["actor"]["entitySearch"]["results"]["entities"]

        # Append the entities to the entities list
        try:
            for entity in entities:
                logging.info(f"Appending entity: {entity['name']}")
                self.entities.append(entity)
        except KeyError:
            logging.error("KeyError: 'name' not found in entity.")

        return next_cursor
