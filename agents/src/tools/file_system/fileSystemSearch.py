import os
import fnmatch
import json

class fileSystemSearch():

    def __init__(self, arguments):
        self.arguments = arguments

    @staticmethod
    def get_definition():
        return {
            "name": "fileSystemSearch",
            "description": "Searches for files and folders based on a pattern.",
            "parameters": {
                "type": "object",
                "properties": {
                    "search_path": {
                        "type": "string",
                        "description": "The path to search in."
                    },
                    "pattern": {
                        "type": "string",
                        "description": "The search pattern, e.g., '*.txt'"
                    }
                },
                "required": ["search_path", "pattern"]
            }
        }

    def run(self, io_handler=None):
        search_path = self.arguments['search_path']
        pattern = self.arguments['pattern']
        matches = []

        if not os.path.exists(search_path):
            return json.dumps({"status": "error", "message": f"Search path '{search_path}' does not exist."})

        try:
            for root, dirs, files in os.walk(search_path):
                for name in files:
                    if fnmatch.fnmatch(name, pattern):
                        matches.append(os.path.join(root, name))
            return json.dumps({"status": "success", "matches": matches})
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})
