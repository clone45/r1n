
import shutil
import json

class fileSystemMoveFolder():

    def __init__(self, arguments):
        self.arguments = arguments

    @staticmethod
    def get_definition():
        return {
            "name": "fileSystemMoveFolder",
            "description": "Moves a folder and all its contents to a new location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_path": {
                        "type": "string",
                        "description": "The current path of the folder."
                    },
                    "destination_path": {
                        "type": "string",
                        "description": "The new path for the folder."
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
            shutil.move(source_path, destination_path)
            return json.dumps({"status": "success", "message": "Folder moved successfully."})
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})
