"""
    This file contains the APIHandler class, which is used to handle the GraphQL API calls
"""
import json
import logging
import os
import requests
from dotenv import load_dotenv

load_dotenv()


class APIHandler:
    def __init__(self):
        self.api_key = os.getenv("NEW_RELIC_API_KEY")
        self.url = "https://api.newrelic.com/graphql"

    def _build_headers(self):
        return {
            "Content-Type": "application/json",
            "API-Key": self.api_key
        }

    def execute_query(self, query, variables=None):
        """
        This function executes a GraphQL query against the New Relic API
        :param query: The GraphQL query to execute
        :param variables: The variables to pass to the query
        :return: The JSON response from the API
        """

        payload = {"query": query}

        if variables:
            payload["variables"] = variables

        headers = self._build_headers()

        try:
            logging.info(f"Sending request with {variables} to the GraphQL endpoint {self.url}")
            response = requests.post(self.url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logging.error(f"API request failed with status code {response.status_code}: {response.text}")
            return None
        except requests.exceptions.RequestException as e:
            logging.error("API request failed due to a network error")
            return None

        return response.json()
