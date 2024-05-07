
import os
import json

class fileSystemChangePermissions():
    @staticmethod
    def get_definition():
        return {
            "name": "fileSystemChangePermissions",
            "description": "Changes the permissions of a file or folder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The path of the file or folder."
                    },
                    "mode": {
                        "type": "integer",
                        "description": "The permission mode (octal number) to set."
                    }
                },
                "required": ["path", "mode"]
            }
        }

    def run(self, io_handler=None):
        path = self.arguments['path']
        mode = self.arguments['mode']

        if not os.path.exists(path):
            return json.dumps({"status": "error", "message": f"Path '{path}' does not exist."})

        try:
            os.chmod(path, mode)
            return json.dumps({"status": "success", "message": "Permissions changed successfully."})
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})
