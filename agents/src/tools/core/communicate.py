
import json
# import pika
# from datetime import datetime
# from src.io.rabbit_mq_io_handler import RabbitMQIOHandler

class communicate():

    def __init__(self, arguments):
        self.arguments = arguments

    @staticmethod
    def get_definition():
        return {
            "name": "communicate",
            "description": """You, the LLM, should use this tool to communicate with users and other agents. 
                There may be times when you're asked to contact another agent.  When you do this, please don't forget to eventually respond to the original agent or user. 
                Calling this function puts a message on the RabbitMQ queue for the recipient to pick up. 
                This is a non-blocking call, so you should consider the action completed once you've called this function. 
                You will receive a message (if there needs to be a response) from the recipient in your queue, 
                so you don't have to continuously check for a response, and please don't repeat your request.""",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "The message content to send."
                    },
                    "from_name": {
                        "type": "string",
                        "description": "The name of the sender.  This is your name."
                    },
                    "from_queue": {
                        "type": "string",
                        "description": "Your return address.  In other words, your queue name. It's likely to be something like queue_1234"
                    },
                    "to_queue": {
                        "type": "string",
                        "description": "The recipient's queue."
                    },
                    "to_name": {
                        "type": "string",
                        "description": "The name of the recipient.  If you don't know this, you can leave it blank"
                    },
                    "to_persona": {
                        "type": "string",
                        "description": "This may be 'agent' or 'human'.  If you don't know, you can omit it.  If you're sending a message to the user interface, this should be 'human'"
                    },
                },
                "required": ["message", "to_queue", "from_name", "from_queue"]
            }
        }

    def run(self, io_handler=None):

        # Extract arguments provided to the tool
        content = self.arguments.get('content', '(empty message in communicate tool)')
        from_name = self.arguments.get('from_name', 'unknown')
        from_queue = self.arguments.get('from_queue')
        from_persona = "agent"
        to_name = self.arguments.get('to_name', '')
        to_queue = self.arguments.get('to_queue')
        to_persona = self.arguments.get('to_persona', '')

        print(f"communicate: Sending message from {from_name} to {to_queue} with content: {content}")

        # Send the message using the IO handler
        
        cc_queue = "user_interface" if to_queue != "user_interface" else ""

        try:
            io_handler.send_output(
                from_name=from_name,
                from_queue=from_queue,
                from_persona=from_persona,
                to_name=to_name,
                to_queue=to_queue,
                to_persona=to_persona,
                cc_queue=cc_queue,
                message_type="message",
                content=content
            )

            result = {"status": "success", "content": "Message sent successfully."}
        except Exception as e:
            print(f"Error sending message: {e}")
            result = {"status": "error", "content": str(e)}

        return json.dumps(result)
