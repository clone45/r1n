import os
import json

class fileSystemDeleteFile():

    def __init__(self, arguments):
        self.arguments = arguments

    @staticmethod
    def get_definition():
        return {
            "name": "fileSystemDeleteFile",
            "description": "Deletes a specified file from the file system.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path of the file to delete."
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
            os.remove(file_path)
            return json.dumps({"status": "success", "message": "File deleted successfully."})
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})
