
import json

class inspectQueue():

    def __init__(self, arguments):
        self.arguments = arguments

    @staticmethod
    def get_definition():
        return {
            "name": "inspectQueue",
            "description": "Inspects the specified queue to retrieve details such as the number of messages and consumers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "queue": {
                        "type": "string",
                        "description": "The name of the queue to inspect. If not provided, defaults to the handler's queue."
                    }
                },
                "required": []
            }
        }

    def run(self, io_handler=None):
        # Extract the queue name if provided
        queue_name = self.arguments.get('queue')

        # Use the io_handler to inspect the specified queue
        try:
            queue_info = io_handler.inspect_queue(queue=queue_name)
            if queue_info:
                result = {"status": "success", "message": "Queue inspected successfully.", "data": queue_info}
            else:
                result = {"status": "error", "message": "Queue not found or error occurred."}
        except Exception as e:
            result = {"status": "error", "message": str(e)}

        return json.dumps(result)
