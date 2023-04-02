import logging
import os


def get_next_cursor(response):
    """
    This function returns the next cursor from the response.
    :param response: The response from the API.
    :return: The next cursor.
    """
    try:
        next_cursor = response["data"]["actor"]["entitySearch"]["results"]["nextCursor"]
    except KeyError:
        next_cursor = None
        logging.error("Unable to find next cursor in response")

    if next_cursor:
        return next_cursor
    else:
        return None


class EntityInformation:
    def __init__(self):
        self.account_id = os.getenv("ACCOUNT_ID")

    def get_apm_entities(self):
        """
        This function returns the query to get a list of APM entities for a given account.
        :return: The GraphQL query and variables.
        """

        query_variables = {
            "entity_search_query": f"domain = 'APM' AND accountId = '{self.account_id}'"
        }

        graphql_query = """
            query ($entity_search_query: String!) {
              actor {
                entitySearch(query: $entity_search_query) {
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

    def get_apm_entities_next_cursor(self, cursor):
        """
        This function returns the query to get a list of APM entities for a given account.
        :param cursor: The cursor to use for the next page of results.  This is returned in the previous query.
        :return: The GraphQL query and variables.
        """

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

        return graphql_query, query_variables
