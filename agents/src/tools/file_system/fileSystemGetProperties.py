
import os
import json
import time

class fileSystemGetProperties():

    def __init__(self, arguments):
        self.arguments = arguments

    @staticmethod
    def get_definition():
        return {
            "name": "fileSystemGetProperties",
            "description": "Retrieves properties of a file or folder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The path of the file or folder."
                    }
                },
                "required": ["path"]
            }
        }

    def run(self, io_handler=None):
        path = self.arguments['path']

        if not os.path.exists(path):
            return json.dumps({"status": "error", "message": f"Path '{path}' does not exist."})

        try:
            properties = {
                "size": os.path.getsize(path),
                "last_modified": time.ctime(os.path.getmtime(path)),
                "last_accessed": time.ctime(os.path.getatime(path)),
                "is_directory": os.path.isdir(path)
            }
            return json.dumps({"status": "success", "properties": properties})
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})
