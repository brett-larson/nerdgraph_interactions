"""
    This module contains the NerdGraphClient class, which is used to execute GraphQL queries against the New Relic API.
"""
import json
import logging
import os
from time import sleep
import requests
from dotenv import load_dotenv

load_dotenv()   # Load environment variables from .env file


class NerdGraphClient:
    """
    This class is used to execute GraphQL queries against the New Relic API.
    """
    def __init__(self):
        """
        This is the constructor for the NerdGraphClient class.
        """
        self.api_key = os.getenv("NEW_RELIC_API_KEY")
        self.url = "https://api.newrelic.com/graphql"
        self.account_id = os.getenv("NEW_RELIC_ACCOUNT_ID")
        self.entities = []  # This will be a list of dictionaries containing entity names and GUIDs

    def _build_headers(self):
        """
        This private function builds the headers for the API request.
        :return: A dictionary containing the headers.
        """

        return {
            "Content-Type": "application/json",
            "API-Key": self.api_key
        }

    def _send_query(self, query, variables=None):
        """
        This private function executes a GraphQL query against the New Relic API. Variables can be passed to the query.
        If no variables are passed, the query will be executed without variables. Executing this function without
        variables will fail if the query requires variables. For this class, variables are required.
        :param query: The NerdGraph query to execute.
        :param variables: The variables to pass to the query.
        :return: The JSON response from the API.
        """

        payload = {"query": query}  # This is the GraphQL query

        if variables:
            payload["variables"] = variables
        else:
            logging.error("Variables must be passed to the query.")
            exit(1)

        headers = self._build_headers() # Build the headers for the API request

        try:
            logging.info(f"Sending request with {variables} to the GraphQL endpoint {self.url}")
            response = requests.post(self.url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logging.error(f"API request failed with status code {response.status_code}: {response.text}")
            logging.error(e)
            exit(1)
        except requests.exceptions.RequestException as e:
            logging.error("API request failed due to a network error")
            logging.error(e)
            exit(1)

        return response.json()

    def build_queries(self, cursor=None):
        """
        This function returns the query to get a list of APM entities for a given account.
        :return: The GraphQL query and variables.
        """

        if cursor:
            query_variables = {
                "entity_search_query": f"domain = 'APM' AND accountId = '{self.account_id}'",
                "cursor": cursor
            }

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
            query_variables = {
                "entity_search_query": f"domain = 'APM' AND accountId = '{self.account_id}'"
            }

            print(query_variables)

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

    def get_entities(self):
        """
        This function returns a list of entities for a given account.
        :return: A list of entities.
        """

        query, variables = self.build_queries()

        response = self._send_query(query, variables)

        next_cursor = self._process_response(response)

        while next_cursor:
            query, variables = self.build_queries(next_cursor)
            response = self._send_query(query, variables)
            next_cursor = self._process_response(response)
            sleep(0.5)

        return self.entities

    def _process_response(self, response):
        """
        This private function processes the response from the API request.
        :param response: The JSON response from the API request.
        :return: The JSON response from the API request.
        """

        next_cursor = response["data"]["actor"]["entitySearch"]["results"]["nextCursor"]
        entities = response["data"]["actor"]["entitySearch"]["results"]["entities"]

        for entity in entities:
            self.entities.append(entity)

        return next_cursor