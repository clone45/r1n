
import os
import json
import logging

class deleteStorage():

    def __init__(self, arguments):
        self.arguments = arguments

    @staticmethod
    def get_definition():
        return {
            "name": "deleteStorage",
            "description": "Delete a specified file within the storage folder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_name": {
                        "type": "string",
                        "description": "The name of the file to delete from the storage folder."
                    }
                },
                "required": ["file_name"]
            }
        }

    def run(self, io_handler=None):
        file_name = self.arguments['file_name']
        storage_file = os.path.join('storage', file_name)
        if not os.path.exists(storage_file):
            return f"File '{file_name}' does not exist in storage."

        try:
            os.remove(storage_file)
            return f"File '{file_name}' has been deleted."
        except Exception as e:
            return f"Error deleting file '{file_name}': {str(e)}"
