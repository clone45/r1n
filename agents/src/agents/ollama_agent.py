import ollama
from src.tools.tool_manager import ToolManager
from .agent import Agent
import json
import logging
import time

class OllamaAgent(Agent):

    def __init__(self, agent_config, instance_uuid, name, avatar, llm, role_folder, reset_assistant, thread, io_handler):
        super().__init__(agent_config, instance_uuid, name, avatar, llm, role_folder, reset_assistant, thread, io_handler)

        self._io_handler = io_handler


    def interact(self, message_json):

        # Extract the content from the message
        content = message_json.get('content', "")
        from_name = message_json.get('from_name', "")
        from_queue = message_json.get('from_queue', "")        
        from_persona = message_json.get('from_persona', "")
        cc_queue = message_json.get('cc_queue', "")

        response = None

        #
        # Call the LLM
        #

        try:

            response = self.llm.run(
                content=content, 
                io_handler=self.io_handler
            )

        except Exception as e:
            logging.error(f"ollama_agent.py::interact - Error calling the llm: {e}")

            # search the error message for the string "No connection could be made", 
            # if found, then send output to the "user_interface" queue alerting the user
            if "No connection could be made" in str(e):
                self._io_handler.send_output(
                    from_name=self.name,
                    from_queue=self.queue,
                    from_persona="agent",
                    to_name="User Interface",
                    to_queue="user_interface",
                    to_persona="user",
                    cc_queue="",
                    message_type="message",
                    content="The ollama LLM is not available.  Have you started it?"
                )
                return

            time.sleep(1)

        # 
        # Send the response back to the agent
        #
        
        if response is not None:
            self._io_handler.send_output(
                from_name=self.name,
                from_queue=self.queue,
                from_persona="agent",
                to_name=from_name,
                to_queue=from_queue,
                to_persona=from_persona,
                cc_queue=cc_queue,
                message_type="message",
                content=response['message']['content']
            )