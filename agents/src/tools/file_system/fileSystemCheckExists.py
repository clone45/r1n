
import os
import json

class fileSystemCheckExists():
    @staticmethod
    def get_definition():
        return {
            "name": "fileSystemCheckExists",
            "description": "Checks if a file or folder exists.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The path to check."
                    }
                },
                "required": ["path"]
            }
        }

    def run(self, io_handler=None):
        path = self.arguments['path']
        exists = os.path.exists(path)
        return json.dumps({"status": "success", "exists": exists})
