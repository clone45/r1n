
import os
import json

class fileSystemRenameFolder():

    def __init__(self, arguments):
        self.arguments = arguments

    @staticmethod
    def get_definition():
        return {
            "name": "fileSystemRenameFolder",
            "description": "Renames a specified folder/directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "current_name": {
                        "type": "string",
                        "description": "The current name/path of the folder."
                    },
                    "new_name": {
                        "type": "string",
                        "description": "The new name/path for the folder."
                    }
                },
                "required": ["current_name", "new_name"]
            }
        }

    def run(self, io_handler=None):
        current_name = self.arguments['current_name']
        new_name = self.arguments['new_name']

        if not os.path.exists(current_name) or not os.path.isdir(current_name):
            return json.dumps({"status": "error", "message": f"Folder '{current_name}' does not exist or is not a directory."})

        try:
            os.rename(current_name, new_name)
            return json.dumps({"status": "success", "message": "Folder renamed successfully."})
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})
