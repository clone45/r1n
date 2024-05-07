
import os
import json

class fileSystemListFolderRecursive():

    def __init__(self, arguments):
        self.arguments = arguments

    @staticmethod
    def get_definition():
        return {
            "name": "fileSystemListFolderRecursive",
            "description": "Recursively lists all files and subfolders within a specified folder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "folder_path": {
                        "type": "string",
                        "description": "The path of the folder to recursively list contents of."
                    }
                },
                "required": ["folder_path"]
            }
        }

    def run(self, io_handler=None):
        folder_path = self.arguments['folder_path']

        if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
            return json.dumps({"status": "error", "message": f"Folder '{folder_path}' does not exist or is not a directory."})

        try:
            contents = []
            for root, dirs, files in os.walk(folder_path):
                for name in files:
                    contents.append(os.path.join(root, name))
                for name in dirs:
                    contents.append(os.path.join(root, name))

            return json.dumps({"status": "success", "contents": contents})
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})
