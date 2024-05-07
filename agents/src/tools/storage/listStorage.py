
import os
import json
import logging

class listStorage():

    def __init__(self, arguments):
        self.arguments = arguments

    @staticmethod
    def get_definition():
        return {
            "name": "listStorage",
            "description": "List all files within the storage folder.",
            "parameters": {
                # No parameters required for listing files
            }
        }

    def run(self, io_handler=None):
        storage_directory = 'storage'
        try:
            # List all files in the directory and return the list
            files = os.listdir(storage_directory)
            return json.dumps(files)
        except Exception as e:
            return f"Error accessing storage directory: {str(e)}"
