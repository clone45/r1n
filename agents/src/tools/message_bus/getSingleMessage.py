
import json

class getSingleMessage():

    def __init__(self, arguments):
        self.arguments = arguments

    @staticmethod
    def get_definition():
        return {
            "name": "getSingleMessage",
            "description": "Fetches a single message from the specified queue.",
            "parameters": {
                "type": "object",
                "properties": {
                    "queue": {
                        "type": "string",
                        "description": "The name of the queue to fetch the message from. If not provided, defaults to the handler's queue."
                    }
                },
                "required": []
            }
        }

    def run(self, io_handler=None):
        # Extract the queue name if provided
        queue_name = self.arguments.get('queue')

        # Use the io_handler to get a single message from the specified queue
        try:
            message = io_handler.get_single_message(queue=queue_name)
            if message:
                result = {"status": "success", "message": "Message fetched successfully.", "data": message}
            else:
                result = {"status": "success", "message": "No messages in the queue."}
        except Exception as e:
            result = {"status": "error", "message": str(e)}

        return json.dumps(result)
