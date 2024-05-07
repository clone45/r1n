
import os
import json

class fileSystemReadFile():

    def __init__(self, arguments):
        self.arguments = arguments

    @staticmethod
    def get_definition():
        return {
            "name": "fileSystemReadFile",
            "description": "Reads the contents of a specified file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path of the file to read."
                    }
                },
                "required": ["file_path"]
            }
        }

    def run(self, io_handler=None):
        file_path = self.arguments['file_path']
        if not os.path.exists(file_path):
            return json.dumps({"status": "error", "message": f"File '{file_path}' does not exist."})

        try:
            with open(file_path, 'r') as file:
                data = file.read()
            return json.dumps({"status": "success", "data": data})
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})
