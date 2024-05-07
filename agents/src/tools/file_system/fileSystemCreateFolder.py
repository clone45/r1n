
import os
import json

class fileSystemCreateFolder():

    def __init__(self, arguments):
        self.arguments = arguments

    @staticmethod
    def get_definition():
        return {
            "name": "fileSystemCreateFolder",
            "description": "Creates a new folder/directory in a specified location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "folder_path": {
                        "type": "string",
                        "description": "The path of the folder to create."
                    }
                },
                "required": ["folder_path"]
            }
        }

    def run(self, io_handler=None):
        folder_path = self.arguments['folder_path']
        if os.path.exists(folder_path):
            return json.dumps({"status": "error", "message": f"Folder '{folder_path}' already exists."})

        try:
            os.makedirs(folder_path)
            return json.dumps({"status": "success", "message": "Folder created successfully."})
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})
