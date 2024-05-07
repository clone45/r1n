
import shutil
import json
import os

class fileSystemCopyFile():
    @staticmethod
    def get_definition():
        return {
            "name": "fileSystemCopyFile",
            "description": "Copies a file from one location to another.",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_path": {
                        "type": "string",
                        "description": "The path of the source file."
                    },
                    "destination_path": {
                        "type": "string",
                        "description": "The path to where the file should be copied."
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
            shutil.copy(source_path, destination_path)
            return json.dumps({"status": "success", "message": "File copied successfully."})
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})
