"""
    This query returns a list of all entity names and their corresponding GUIDs.
"""

import json
import logging
import shared.NerdGraphClient as NerdGraphClient
from queries.entity_names_guids import EntityCollector
import newrelic.agent


@newrelic.agent.background_task()
def get_entity_names_guids():
    """
    This is the main method for the application. Primary variables and control flow are here.
    :return: No data returned.
    """

    logging.info("Starting process to collect Entity Names and GUIDs.")

    nerdgraph = NerdGraphClient.NerdGraphClient()
    entities = EntityCollector.EntityCollector()

    entity_list = entities.get_entities(nerdgraph)

    logging.info("Finished process to collect Entity Names and GUIDs.")

    return entity_list
