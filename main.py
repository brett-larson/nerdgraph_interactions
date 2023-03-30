"""
    This is the main file for the application. It contains the main method and control flow.
"""

import logging
from time import sleep
import APIHandler
import APMQueryHandler

# Configure logging
logging.basicConfig(
    filename="application.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filemode="w"
)


def main():
    """
    This is the main method for the application. Primary variables and control flow are here.
    :return: No data returned.
    """

    logging.info("Starting the application.")
    entity_list = []  # List to store entity dictionaries

    # Create instances of the APIHandler and APMQueryHandler classes
    api_handler = APIHandler.APIHandler()
    apm_query_handler = APMQueryHandler.APMQueryHandler()

    # Get the GraphQL query and variables
    query, variables = apm_query_handler.get_apm_entities()

    # Execute the query
    logging.info("Executing query to get APM entities.")
    result = api_handler.execute_query(query, variables)

    # Get the next cursor
    next_cursor = result["data"]["actor"]["entitySearch"]["results"]["nextCursor"]
    logging.info(f"Next cursor: {next_cursor}")

    # Get the list of entities and append to the entity_list
    entities = result["data"]["actor"]["entitySearch"]["results"]["entities"]
    for entity in entities:
        entity_list.append(entity)

    # Loop through the next cursors until there are no more cursors
    while next_cursor:
        query, variables = apm_query_handler.get_apm_entities_next_cursor(next_cursor)
        result = api_handler.execute_query(query, variables)

        # Get the next cursor
        next_cursor = result["data"]["actor"]["entitySearch"]["results"]["nextCursor"]
        logging.info(f"Next cursor: {next_cursor}")

        # Get the list of entities and append to the entity_list
        entities = result["data"]["actor"]["entitySearch"]["results"]["entities"]
        for entity in entities:
            entity_list.append(entity)

        sleep(0.5)  # Sleep for 0.5 seconds to avoid rate limiting

    # Get the average response time for each entity
    for entity in entity_list:
        query, variables = apm_query_handler.get_apm_avg_transaction_time(entity["guid"])
        result = api_handler.execute_query(query, variables)

        # Get the average response time
        avg_response_time = result["data"]["actor"]["nrql"]["results"][0]["average.duration"]
        entity["avg_response_time"] = avg_response_time

        sleep(0.5)  # Sleep for 0.5 seconds to avoid rate limiting

    # Print the list of entities with the average response time
    print(entity_list)

    logging.info("Application has completed all tasks.")


if __name__ == '__main__':
    main()
