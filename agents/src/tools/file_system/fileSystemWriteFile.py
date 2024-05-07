
import os
import json

class fileSystemWriteFile():

    def __init__(self, arguments):
        self.arguments = arguments

    @staticmethod
    def get_definition():
        return {
            "name": "fileSystemWriteFile",
            "description": "Writes or appends data to a specified file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path of the file to write or append to."
                    },
                    "data": {
                        "type": "string",
                        "description": "The data to write to the file."
                    },
                    "mode": {
                        "type": "string",
                        "enum": ["write", "append"],
                        "description": "The mode to open the file: 'write' or 'append'."
                    }
                },
                "required": ["file_path", "data", "mode"]
            }
        }

    def run(self, io_handler=None):
        file_path = self.arguments['file_path']
        data = self.arguments['data']
        mode = self.arguments['mode']

        try:
            with open(file_path, 'w' if mode == "write" else 'a') as file:
                file.write(data)
            return json.dumps({"status": "success", "message": "File written successfully."})
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})
