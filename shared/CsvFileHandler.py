"""
    This module contains the CsvFileHandler class.
"""

import csv
import logging
import os
import sys

import newrelic.agent


class CsvFileHandler:
    """ This class handles the csv file. """

    def __init__(self, file_name):
        """ Initialize the class. """
        self.file_name = file_name
        self.class_directory = os.path.dirname(os.path.realpath(__file__))
        self.parent_directory = os.path.dirname(self.class_directory)
        self.csv_directory = 'csv_files'
        self.csv_files_directory = os.path.join(self.parent_directory, self.csv_directory, self.file_name)

    @newrelic.agent.background_task(name="read_file", group="Task")
    def read_file(self):
        """
        Read the csv file.
        :return: A list of lists.
        """
        try:
            logging.info("Reading the CSV file.")
            with open(self.file_name, 'r') as file:
                csv_reader = csv.reader(file)
                file.close()
        except FileNotFoundError:
            logging.error(f"File not found: {self.file_name}. Exiting the application.")
            sys.exit()

        return list(csv_reader)

    @newrelic.agent.background_task(name="write_csv", group="Task")
    def write_csv(self, data, as_dict=False):
        """
        Write the csv file. The data can be a list of dictionaries or a list.
        :param data: A list of dictionaries or a list.
        :param as_dict: A boolean value indicating whether the data is a list of dictionaries or a list.
        :return:  No data returned.
        """

        try:
            if as_dict:
                logging.info("Writing the CSV file as a dictionary.")
                fieldnames = list(data[0].keys())
                with open(self.csv_files_directory, mode='w', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    for row in data:
                        writer.writerow(row)
                    file.close()
            else:
                logging.info("Writing the CSV file as a list.")
                with open(self.csv_files_directory, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    for row in data:
                        writer.writerow(row)
                    file.close()
        except IOError as e:
            logging.error(f"Error writing the CSV file. Exiting the application.")
            logging.error(e)
            sys.exit()
        except ValueError as e:
            logging.error(f"Error writing the CSV file. Exiting the application.")
            logging.error(e)
            sys.exit()
        except Exception as e:
            logging.error(f"Error writing the CSV file. Exiting the application.")
            logging.error(e)
            sys.exit()

    @newrelic.agent.background_task(name="append_file", group="Task")
    def append_file(self, data):
        """
        Append the csv file.
        :param data: A list of data to append to the csv file.
        :return: No data returned.
        """

        try:
            with open(self.file_name, 'a') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(data)
        except FileNotFoundError:
            logging.error(f"File not found: {self.file_name}. Exiting the application.")
            sys.exit()

    @newrelic.agent.background_task(name="delete_file", group="Task")
    def delete_file(self):
        """
        Delete the csv file.
        :return: No data returned.
        """

        logging.info("Deleting the CSV file.")
        try:
            os.remove(self.file_name)
        except FileNotFoundError:
            logging.error(f"File not found: {self.file_name}. Exiting the application.")
            sys.exit()
