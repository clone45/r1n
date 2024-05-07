
import os
import json

class fileSystemCreateSymbolicLink():

    def __init__(self, arguments):
        self.arguments = arguments

    @staticmethod
    def get_definition():
        return {
            "name": "fileSystemCreateSymbolicLink",
            "description": "Creates a symbolic link to a file or folder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "target_path": {
                        "type": "string",
                        "description": "The path of the target file or folder."
                    },
                    "link_path": {
                        "type": "string",
                        "description": "The path for the symbolic link."
                    }
                },
                "required": ["target_path", "link_path"]
            }
        }

    def run(self, io_handler=None):
        target_path = self.arguments['target_path']
        link_path = self.arguments['link_path']

        if not os.path.exists(target_path):
            return json.dumps({"status": "error", "message": f"Target '{target_path}' does not exist."})

        try:
            os.symlink(target_path, link_path)
            return json.dumps({"status": "success", "message": f"Symbolic link created at '{link_path}' pointing to '{target_path}'."})
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})
