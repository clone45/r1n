import json
import logging
from bson.json_util import default
from dotenv import load_dotenv
from src.repositories.PresenseRepository import PresenceRepository

class Agent:

    def __init__(self, instance_uuid, profile, llm, role, reset_assistant, thread, io_handler):

        self.llm = llm
        self.presence_repository = PresenceRepository()

        # The IO handler and message logger is passed in so that it can be accessed by 
        # the tools.  This is necessary because the 'communicate' tool (tools/core/communicate.py) need to use the IO handler to send messages.

        self.instance_uuid = instance_uuid
        self.io_handler = io_handler
        self.thread = thread
        self.profile = profile
        self.role = role

        self.queue = f"queue_{instance_uuid}"

        load_dotenv()

        # Extract some useful information from the agent_config
        self.capabilities = self.role.get('capabilities', "")

        # TODO: This could probably be moved up into run.py
        if(self.profile['avatar'] == ""):
            self.profile['avatar'] = self.role.get('avatar', 'images/profiles/default.png')

        # Notify the web interface of the new agent
        self.notify_ui_of_new_agent()


    def get_role(self):
        return self.role

    #
    # Todo: instead of notifying the user interface directly like this, instead allow for
    # the user interface to subscribe to agent events.  This code will then iterate over the
    # subscribers and notify them of the event.
    
    def notify_ui_of_removed_agent(self):

        agent_info_string = json.dumps({
            "name": self.profile['name'],
            "queue": self.queue,
            "instance_uuid": self.instance_uuid
        }, default=default)

        self.io_handler.send_output(
            from_name=self.profile['name'],
            from_queue=self.queue,
            from_persona="system",
            to_name="User Interface Server",
            to_queue="user_interface",
            to_persona="system",
            cc_queue="",
            content=agent_info_string,
            message_type="ui.remove_agent"
        )

    def notify_ui_of_new_agent(self):
            
        # Create a json string of the agent's name, queue, and capabilities
        agent_info_string = json.dumps({
            "name": self.profile['name'],
            "profile": self.profile,
            "queue": self.queue,
            "role": self.role,
            "capabilities": self.capabilities,
            "instance_uuid": self.instance_uuid
        }, default=default)

        print("Notifying UI of new agent..." + agent_info_string)
        
        # Send the agent info to the web interface
        self.io_handler.send_output(
            from_name=self.profile['name'],
            from_queue=self.queue,
            from_persona="system",
            to_name="User Interface Server",
            to_queue="user_interface",
            to_persona="system",
            cc_queue="",
            content=agent_info_string,
            message_type="ui.add_agent"
        )

    def notify_ui_of_thinking_started(self):
        agent_info_string = json.dumps({
            "name": self.profile['name'],
            "queue": self.queue,
            "instance_uuid": self.instance_uuid
        }, default=default)

        self.io_handler.send_output(
            from_name=self.profile['name'],
            from_queue=self.queue,
            from_persona="system",
            to_name="User Interface Server",
            to_queue="user_interface",
            to_persona="system",
            cc_queue="",
            content=agent_info_string,
            message_type="ui.agent_thinking_started"
        )

    def notify_ui_of_thinking_completed(self):
        agent_info_string = json.dumps({
            "name": self.profile['name'],
            "queue": self.queue,
            "instance_uuid": self.instance_uuid
        }, default=default)

        self.io_handler.send_output(
            from_name=self.profile['name'],
            from_queue=self.queue,
            from_persona="system",
            to_name="User Interface Server",
            to_queue="user_interface",
            to_persona="system",
            cc_queue="",
            content=agent_info_string,
            message_type="ui.agent_thinking_completed"
        )

    def send_pong_to_ui(self):
        self.io_handler.send_output(
            from_name=self.profile['name'],
            from_queue=self.queue,
            from_persona="system",
            to_name="User Interface Server",
            to_queue="user_interface",
            to_persona="system",
            cc_queue="",
            content="pong",
            message_type="ui.pong"
        )    

    def register_presence(self):
        # self._agent_presence_manager.add_or_update_agent(self.instance_uuid, self.queue, self.profile)
        self.presence_repository.add({
            "agent_instance_uuid": self.instance_uuid,
            "queue_name": self.queue,
            "profile": self.profile
        })

    def shutdown(self, input_message=None):

        print("Agent shutting down...")

        self.notify_ui_of_removed_agent()

        # Gracefully shutdown the IO handler
        self.io_handler.graceful_shutdown()


    def read(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            logging.error(f"__Error reading file in agent.py: {filename}: {e}")
            return None

