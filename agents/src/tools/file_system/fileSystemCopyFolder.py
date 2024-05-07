
import shutil
import json
import os

class fileSystemCopyFolder():
    @staticmethod
    def get_definition():
        return {
            "name": "fileSystemCopyFolder",
            "description": "Copies a folder and all its contents to a new location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_path": {
                        "type": "string",
                        "description": "The path of the source folder."
                    },
                    "destination_path": {
                        "type": "string",
                        "description": "The path to where the folder should be copied."
                    }
                },
                "required": ["source_path", "destination_path"]
            }
        }

    def run(self, io_handler=None):
        source_path = self.arguments['source_path']
        destination_path = self.arguments['destination_path']

        if not os.path.exists(source_path) or not os.path.isdir(source_path):
            return json.dumps({"status": "error", "message": f"Source folder '{source_path}' does not exist or is not a directory."})

        try:
            shutil.copytree(source_path, destination_path)
            return json.dumps({"status": "success", "message": "Folder copied successfully."})
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})
