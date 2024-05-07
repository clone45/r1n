
import json
import threading
import uuid
import logging

class setTimer():

    def __init__(self, arguments):
        self.arguments = arguments

    @staticmethod
    def get_definition():
        return {
            "name": "setTimer",
            "description": "Sets a timer to send a message to a specified queue after a duration.",
            "parameters": {
                "type": "object",
                "properties": {
                    "duration": {
                        "type": "integer",
                        "description": "The duration of the timer in seconds."
                    },
                    "reminder": {
                        "type": "string",
                        "description": "The reminder to send when the timer expires."
                    },
                    "from_name": {
                        "type": "string",
                        "description": "The name of the sender.  This is your name."
                    },
                    "from_queue": {
                        "type": "string",
                        "description": "Your return address.  In other words, your queue name. It's likely to be something like queue_1234"
                    },
                    "to_name": {
                        "type": "string",
                        "description": "The name of the recipient.  If you don't know this, you can leave it blank"
                    },
                    "to_queue": {
                        "type": "string",
                        "description": "The recipient's queue."
                    }
                },
                "required": ["duration", "reminder", "from_name", "from_queue", "to_name", "to_queue"]
            }
        }

    def run(self, io_handler=None):

        # todo: A lot more work to do here
        duration = self.arguments.get('duration')
        reminder = self.arguments.get('reminder')
        from_name = self.arguments.get('from_name')
        from_queue = self.arguments.get('from_queue')
        to_name = self.arguments.get('to_name')
        to_queue = self.arguments.get('to_queue')

        timer_id = str(uuid.uuid4())

        # append timer id to message
        message = f"Timer ID: {timer_id} completed with message: {reminder}"

        def timer_action(message):
            try:
                io_handler.send_output(
                    from_name=from_name,
                    from_queue=from_queue,
                    from_persona="agent",
                    to_name=to_name,
                    to_queue=to_queue,
                    to_persona="agent",
                    cc_queue="",
                    message_type="message",
                    content="Reminder: " + reminder
                )
                logging.info(f"__Timer {timer_id} completed with message: {reminder}")
                logging.info(f"__Reminder sent to {to_name} in queue {to_queue}")
            except Exception as e:
                logging.error(f"__An error occurred while sending the reminder: {e}")
                pass

        timer = threading.Timer(duration, timer_action, args=(message,))
        timer.start()

        return json.dumps({"status": "success", "message": "Timer set successfully.", "timer_id": timer_id})
