"""
    This module contains the CsvFileHandler class.
"""

import csv
import os
import sys


class CsvFileHandler:
    """ This class handles the csv file. """

    def __init__(self, file_name):
        """ Initialize the class. """
        self.file_name = file_name

    def read_file(self):
        """ Read the csv file. """
        try:
            with open(self.file_name, 'r') as file:
                csv_reader = csv.reader(file)
                return list(csv_reader)
        except FileNotFoundError:
            print("File not found.")
            sys.exit()

    def write_file(self, data):
        """ Write the csv file. """
        try:
            with open(self.file_name, 'w') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerows(data)
        except FileNotFoundError:
            print("File not found.")
            sys.exit()

    def append_file(self, data):
        """ Append the csv file. """
        try:
            with open(self.file_name, 'a') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(data)
        except FileNotFoundError:
            print("File not found.")
            sys.exit()

    def delete_file(self):
        """ Delete the csv file. """
        try:
            os.remove(self.file_name)
        except FileNotFoundError:
            print("File not found.")
            sys.exit()
