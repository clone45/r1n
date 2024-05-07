
import os
import shutil
import json

class fileSystemDeleteFolder():

    def __init__(self, arguments):
        self.arguments = arguments

    @staticmethod
    def get_definition():
        return {
            "name": "fileSystemDeleteFolder",
            "description": "Deletes a specified folder/directory from the file system.",
            "parameters": {
                "type": "object",
                "properties": {
                    "folder_path": {
                        "type": "string",
                        "description": "The path of the folder to delete."
                    },
                    "recursive": {
                        "type": "boolean",
                        "description": "Whether to delete the folder recursively."
                    }
                },
                "required": ["folder_path", "recursive"]
            }
        }

    def run(self, io_handler=None):
        folder_path = self.arguments['folder_path']
        recursive = self.arguments['recursive']

        if not os.path.exists(folder_path):
            return json.dumps({"status": "error", "message": f"Folder '{folder_path}' does not exist."})

        try:
            if recursive:
                shutil.rmtree(folder_path)
            else:
                os.rmdir(folder_path)
            return json.dumps({"status": "success", "message": "Folder deleted successfully."})
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})
