"""
    This is the main file for the application. It contains the main method and control flow.
"""

import logging
import queries.entity_names_guids.get_entity_names_guids as get_entities

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

    logging.info("Starting the NerdGraph Interactions application.")

    entities = get_entities.get_entity_names_guids()
    print(entities)

    logging.info("Finished the NerdGraph Interactions application.")


if __name__ == '__main__':
    main()
