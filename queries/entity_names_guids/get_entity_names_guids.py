"""
    This query returns a list of all entity names and their corresponding GUIDs.
"""

import json
import logging
import NerdGraphClient
from queries.entity_names_guids import EntityCollection


def get_entity_names_guids():
    """
    This is the main method for the application. Primary variables and control flow are here.
    :return: No data returned.
    """

    logging.info("Starting process to collect Entity Names and GUIDs.")

    nerdgraph = NerdGraphClient.NerdGraphClient()   # Instantiate the NerdGraphClient class
    entities = EntityCollection.EntityCollection()  # Instantiate the EntityCollection class

    entity_list = entities.get_entities(nerdgraph)

    logging.info("Finished process to collect Entity Names and GUIDs.")

    return entity_list
