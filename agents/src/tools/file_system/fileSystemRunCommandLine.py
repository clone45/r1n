
import subprocess
import json

class fileSystemRunCommandLine():

    def __init__(self, arguments):
        self.arguments = arguments

    @staticmethod
    def get_definition():
        return {
            "name": "fileSystemRunCommandLine",
            "description": "Executes a command in the command line and returns its output.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The command line command to execute."
                    }
                },
                "required": ["command"]
            }
        }

    def run(self, io_handler=None):
        command = self.arguments['command']

        try:
            # Run the command and capture the output
            result = subprocess.run(command, shell=True, text=True, capture_output=True, check=True)
            return json.dumps({"status": "success", "output": result.stdout})
        except subprocess.CalledProcessError as e:
            # If the command fails, capture the error message
            return json.dumps({"status": "error", "message": e.stderr})
        except Exception as e:
            # Handle other exceptions
            return json.dumps({"status": "error", "message": str(e)})
