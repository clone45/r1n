
import json

class agentShutdown():

    def __init__(self, arguments):
        self.arguments = arguments

    @staticmethod
    def get_definition():
        return {
            "name": "agentShutdown",
            "description": """Use this tool to shutdown an agent.  You can use this also to shutdown yourself if asked.  This tool sends a request to the GuestbookService to remove the agent from the guestbook and then sends a message to the agent to shutdown.  If you are using this tool to shutdown yourself, you should expect to be removed from the guestbook and then receive a message to shutdown.  If you are using this tool to shutdown another agent, you should expect the other agent to be removed from the guestbook and then receive a message to shutdown.  This is a non-blocking call, so you should consider the action completed once you've called this function.  You will receive a message (if there needs to be a response) from the recipient in your queue, so you don't have to continuously check for a response, and please don't repeat your request.""",
            "parameters": {
                "type": "object",
                "properties": {
                    "transaction_id": {
                        "type": "string",
                        "description": "A transaction id should be provided for debugging purposes.  If not provided, provide the string 'None'."
                    },
                    "sender_name": {
                        "type": "string",
                        "description": "The name of the sender.  If you are sending the message, this is your name."
                    },
                    "return_address": {
                        "type": "string",
                        "description": "Your return address"
                    },
                    "agent_queue": {
                        "type": "string",
                        "description": "The queue of the agent to shutdown.  This is also called the return address of the agent.  Don't put your own return address here unless you are shutting down yourself."
                    }
                },
                "required": ["message", "sender_name", "return_address", "agent_queue"]
            }
        }

    def run(self, io_handler=None):

        # Extract transaction_id if provided
        # transaction_id = self.arguments.get('transaction_id', 'None')
        sender_name = self.arguments.get('sender_name')
        return_address = self.arguments.get('return_address')
        agent_queue = self.arguments.get('agent_queue')

        # Send the request to read the guestbook
        try:
            io_handler.send_output(
                content=agent_queue, 
                sender_name=sender_name,
                return_address=return_address,
                recipient_queue="guestbook_service",
                message_type="agent.shutdown")

            result = {"status": "success", f"content": "Guestbook got shutdown request for {agent_queue}"}
        except Exception as e:
            result = {"status": "error", "content": str(e)}

        return json.dumps(result)
