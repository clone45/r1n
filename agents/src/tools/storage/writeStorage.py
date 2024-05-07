
import os
import json
import logging

class writeStorage():
    
    def __init__(self, arguments):
        self.arguments = arguments

    @staticmethod
    def get_definition():
        return {
            "name": "writeStorage",
            "description": "Write data to a specified file within the storage folder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_name": {
                        "type": "string",
                        "description": "The name of the file to write to in the storage folder."
                    },
                    "data": {
                        "type": "string",
                        "description": "The data to write to the file."
                    }
                },
                "required": ["file_name", "data"]
            }
        }

    def run(self, io_handler=None):
        file_name = self.arguments['file_name']
        data = self.arguments['data']
        storage_file = os.path.join('storage', file_name)

        # Ensure the storage directory exists
        os.makedirs(os.path.dirname(storage_file), exist_ok=True)

        try:
            with open(storage_file, 'w') as file:
                file.write(data)
            return f"Data successfully written to '{file_name}'."
        except Exception as e:
            return f"Error writing to file '{file_name}': {str(e)}"
