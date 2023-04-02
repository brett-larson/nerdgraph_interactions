"""
    This is the main file for the application. It contains the main method and control flow.
"""

import logging
from time import sleep
import NerdGraphClient

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

    nerdgraph_client = NerdGraphClient.NerdGraphClient()

    entity_list = nerdgraph_client.get_entities()
    print(entity_list)


if __name__ == '__main__':
    main()
