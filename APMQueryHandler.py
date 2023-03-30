"""
    This file contains the APMQueryHandler class.
"""

import os


class APMQueryHandler:
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

    def get_apm_avg_transaction_time(self, entity_guid):
        """
        This function returns the query to get the average transaction time for a given APM entity.
        :param entity_guid: The entity GUID.
        :return: The GraphQL query and variables.
        """

        account_int = int(self.account_id)

        nrql_query = f"FROM Transaction SELECT average(duration) WHERE entityGuid = '{entity_guid}'"

        query_variables = {
            "account": account_int,
            "query": nrql_query
        }

        graphql_query = """
            query ($query: Nrql!, $account:Int!) {
              actor {
                nrql(query: $query, accounts: $account) {
                  results
                }
              }
            }
            """

        return graphql_query, query_variables
