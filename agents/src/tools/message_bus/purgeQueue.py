
import json

class purgeQueue():

    def __init__(self, arguments):
        self.arguments = arguments

    @staticmethod
    def get_definition():
        return {
            "name": "purgeQueue",
            "description": "Clears all messages from the specified queue.",
            "parameters": {
                "type": "object",
                "properties": {
                    "queue": {
                        "type": "string",
                        "description": "The name of the queue to be purged. If not provided, defaults to the handler's queue."
                    }
                },
                "required": []
            }
        }

    def run(self, io_handler=None):
        # Extract the queue name if provided
        queue_name = self.arguments.get('queue')

        # Use the io_handler to purge the specified queue
        try:
            io_handler.purge_queue(queue=queue_name)
            result = {"status": "success", "message": f"All messages in queue '{queue_name}' have been cleared."}
        except Exception as e:
            result = {"status": "error", "message": str(e)}

        return json.dumps(result)
