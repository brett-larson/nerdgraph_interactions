"""
    This query returns a list of all entity names and their corresponding GUIDs.
"""

import json
import logging
import NerdGraphClient
from queries.average_transaction_duration import EntityAvgDurationCollector


def get_entity_average_transaction_duration(entity_list):
    """
    This is the main method for the application. Primary variables and control flow are here.
    :return: No data returned.
    """

    logging.info("Starting process to collect Entity Names and GUIDs.")

    nerdgraph = NerdGraphClient.NerdGraphClient()
    average_duration = EntityAvgDurationCollector.EntityAvgDurationCollector()

    entity_list = average_duration.get_average_entity_duration(entity_list, nerdgraph)

    logging.info("Finished process to collect Entity Names and GUIDs.")

    return entity_list
