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
