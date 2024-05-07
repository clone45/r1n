
import subprocess
import json
import logging

class shellExecutor():

    def __init__(self, arguments):
        self.arguments = arguments

    @staticmethod
    def get_definition():
        return {
            "name": "shellExecutor",
            "description": "Execute a command in the Windows command line and return its output.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The command to be executed in the command line."
                    }
                },
                "required": ["command"]
            }
        }

    def run(self, io_handler=None):
        command = self.arguments['command']
        try:
            # Using subprocess to execute the command
            result = subprocess.run(command, shell=True, text=True, capture_output=True, check=True)
            return json.dumps({"status": "success", "output": result.stdout})
            
        except subprocess.CalledProcessError as e:
            logging.error(f"Command line execution error: {str(e)}")
            return json.dumps({"status": "error", "message": str(e), "output": e.output})
