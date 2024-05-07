
import os
import json

class fileSystemMoveFile():

    def __init__(self, arguments):
        self.arguments = arguments

    @staticmethod
    def get_definition():
        return {
            "name": "fileSystemMoveFile",
            "description": "Moves a file from one location to another. This can also be used for renaming files.",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_path": {
                        "type": "string",
                        "description": "The current path of the file."
                    },
                    "destination_path": {
                        "type": "string",
                        "description": "The new path for the file."
                    }
                },
                "required": ["source_path", "destination_path"]
            }
        }

    def run(self, io_handler=None):
        source_path = self.arguments['source_path']
        destination_path = self.arguments['destination_path']

        if not os.path.exists(source_path):
            return json.dumps({"status": "error", "message": f"Source file '{source_path}' does not exist."})

        try:
            os.rename(source_path, destination_path)
            return json.dumps({"status": "success", "message": "File moved successfully."})
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})
