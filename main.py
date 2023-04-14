"""
    This is the main file for the application. It contains the main method and control flow.
"""

import logging
import os

from dotenv import load_dotenv

import shared.CsvFileHandler as CsvFileHandler
import queries.entity_names_guids.get_entity_names_guids as get_entities
import queries.average_transaction_duration.get_entity_average_transaction_duration as get_average_duration
import newrelic.agent
newrelic.agent.initialize('newrelic.ini')

# Configure logging
logging.basicConfig(
    filename="application.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filemode="w"
)


@newrelic.agent.background_task()
def main():
    """
    This is the main method for the application. Primary variables and control flow are here.
    :return: No data returned.
    """

    logging.info("Starting the NerdGraph Interactions application.")

    settings_dict = dict(newrelic.agent.global_settings())

    for name, value in settings_dict.items():
        logging.info(f"Setting: {name} = {value}")

    entities = get_entities.get_entity_names_guids()

    entities = get_average_duration.get_entity_average_transaction_duration(entities)

    csv_writer = CsvFileHandler.CsvFileHandler("output.csv")
    csv_writer.write_csv(entities, as_dict=True)

    logging.info("Finished the NerdGraph Interactions application.")


if __name__ == '__main__':
    main()
