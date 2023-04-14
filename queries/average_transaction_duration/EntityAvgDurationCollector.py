"""
    This module contains the NerdGraphClient class, which is used to execute GraphQL queries against the New Relic API.
"""
import json
import logging
import os
from time import sleep

import newrelic.agent
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


class EntityAvgDurationCollector:
    """
    This class contains the methods to get the average transaction duration for a given entity. The
    get_average_transaction_duration method is the primary method called.
    """

    def __init__(self):
        """
        This is the constructor for the NerdGraphClient class.
        """
        self.api_key = os.getenv("NEW_RELIC_API_KEY")
        self.url = "https://api.newrelic.com/graphql"
        self.account_id = os.getenv("NEW_RELIC_ACCOUNT_ID")

    @newrelic.agent.background_task()
    def get_average_entity_duration(self, entity_list, nerdgraph_client):
        """
        This function returns a list of entities for a given account.
        :return: A list of entities.
        """

        for entity in entity_list:
            query, variables = self.build_query(entity["guid"])
            response = nerdgraph_client.send_query(query, variables)
            average_duration = response["data"]["actor"]["nrql"]["results"][0]["average.duration"]
            entity["average_duration"] = average_duration

        return entity_list

    @newrelic.agent.background_task()
    def build_query(self, entity_guid):
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
