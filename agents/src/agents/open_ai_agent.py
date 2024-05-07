# open_ai_agent.py

import json
import time
import os
import logging
from src.logging.logging_config import setup_papertrail_logging
from .agent import Agent
from src.tools.tool_manager import ToolManager
from src.repositories.ProfilesRepository import ProfilesRepository

class OpenAIAgent(Agent):

    def __init__(self, instance_uuid, profile, llm, role, reset_assistant, thread, io_handler):
        super().__init__(instance_uuid, profile, llm, role, reset_assistant, thread, io_handler)

        self._tools = ToolManager()
        self.name = profile['name']
        self.role = role
        self.profile = profile
        self.assistant_id = self.profile.get('assistant_id', None)

        self.profiles_repository = ProfilesRepository()

        # Prepare and configure Papertrail logging
        setup_papertrail_logging('open_ai_agent')
        self.logger = logging.getLogger('open_ai_agent')

        # Load the tools for the role
        tool_names = self.role.get('tools', [])
        tool_definitions = self._tools.load_tools(tool_names)
        
        
        
#        if self._assistant_id is None:
#            self._assistant_id = self.create_assistant(role, tool_definitions)
#        else:
#            # Always update the assistant if it already exists
#            # This is necessary because the assistant may have been updated, such as the instructions or tools
#            self.update_assistant(role, tool_definitions)


    # todo: is it necessary to pass in roll?  Can't we just use self.role?
    def create_assistant(self, role, tool_definitions):
        assistant_config = {
            "instructions": role['instructions'],
            "name": self.role['name'],
            "model": role['model'],
            "tools": tool_definitions
        }
        assistant = self.llm.create_assistant(assistant_config)
        return assistant.id
    
    # todo: is it necessary to pass in roll?  Can't we just use self.role?
    def update_assistant(self, role, tool_definitions):
        assistant_config = {
            "instructions": self.role['instructions'],
            "name": role['name'],
            "model": role['model'],
            "tools": tool_definitions
        }
        self.llm.update_assistant(self.assistant_id, assistant_config)

    # todo: this needs rethinking

    def get_assistant_id(self):
        return self.assistant_id

#    def get_assistant_id(self):
#        # Check if the assistant already exists
#        existing_assistants = self.llm.list_assistants()
#        for assistant in existing_assistants.data:
#            if assistant.name == self.role['name']:
#                return assistant.id
#        return None

    def upload_file(self, incoming_message):

        # example incoming message:
        # {"from_name":"User Interface","from_queue":"user_interface","to_name":"Rin","to_queue":"queue_3820c769-2541-4d15-862a-34dd3f306543","cc_queue":"","message_type":"file.upload","content":"{\"file_path\":\"uploads\\\\file-1714086861692-456514607.txt\",\"file_name\":\"japanesecookingcdkstack-sitebucket3.txt\",\"file_size\":664,\"agent_uuid\":\"3820c769-2541-4d15-862a-34dd3f306543\",\"agent_name\":\"Rin\"}","message_timestamp":1714086861694}


        self.logger.debug(f"upload_file - Incoming message:")
        self.logger.debug(json.dumps(incoming_message))

        content = json.loads(incoming_message['content'])
        
        original_file_name = content['original_file_name']
        file_name = content['file_name']
        file_size = content['file_size']
        agent_uuid = content['agent_uuid']
        agent_name = content['agent_name']
        context = content['context'] # either 'agent_list' or 'thread'
        file_path = os.getenv('UPLOADS_PATH', 'uploads') + '/' + file_name

        # use python's pathlib to normalize the path to work on all platforms, plus prepend with ../ to go up one directory
        file_path = os.path.normpath(file_path)

        # Check to see if the file exists.  It should be in ../uploads  (although, TODO: make this configurable via .env and customed for docker)
        if os.path.exists(file_path):           
            self.logger.info(f"open_ai_agent.py::upload_file - File {file_path} exists.")

            # TODO: We need to check the context.  If the context if 'agent_list', then the following code is correct.
            # Otherwise, we need to attach the file to the thread.

            # The profile record may contain a vector_stores array, which is a list of vector store IDs.  If the vector store
            # is not in the profile, then we need to create it.  If it is in the profile, we need to attach it to the assistant.
            # We can assume that the vector store only contains one item, as the assistant should only have one vector store.
            # This might change in the future.

            # Check to see if the vector store exists
            if self.profile.get('vector_stores', None):
                vector_store_id = self.profile['vector_stores'][0]
                vector_store = self.llm.get_vector_store(vector_store_id)
            else:
                params = {
                    "name": agent_name,
                    "metadata": {
                        "agent_uuid": agent_uuid,
                        "agent_name": agent_name
                    }
                }
                vector_store = self.llm.create_vector_store(params)

                # Save the vector store ID to the profile
                self.profile['vector_stores'] = [vector_store.id]

                # Update the profile with the new vector store
                self.profiles_repository.update(self.profile['uuid'], self.profile)

            # Ready the files for upload to OpenAI 
            file_paths = [file_path]
            file_streams = [open(path, "rb") for path in file_paths]

            # Use the upload and poll SDK helper to upload the files, add them to the vector store,
            # and poll the status of the file batch for completion.
            file_batch = self.llm.upload_and_poll(vector_store.id, file_streams)

            # Close the file streams
            for stream in file_streams:
                stream.close()

            # attach vector store to assistant
            self.llm.attach_vector_store_to_assistant(self.assistant_id, vector_store.id)

            self.logger.debug("File batch status:")
            self.logger.debug(file_batch.status)
            self.logger.debug(file_batch.file_counts)

        else:
            self.logger.error(f"upload_file - File {file_path} does not exist.")
            
        

    def reset_assistant(self, role, tool_definitions):
        # TODO: rewrite this
        pass

        #        # Check if the assistant already exists
        #        existing_assistants = self.llm.list_assistants()
        #        for assistant in existing_assistants.data:
        #            if assistant.name == agent_config['role']:
        #                self.llm.delete_assistant(assistant.id)
        #                logging.info(f"Reset assistant {assistant.id}")
        #                break  # Exit the loop once the assistant is deleted
        #
        #        # Create a new assistant
        #        return self.create_assistant(agent_config, tool_definitions)
    
    def interact(self, outbound_message):
        
        if not isinstance(outbound_message, str):
            outbound_message_str = json.dumps(outbound_message)
        else:
            outbound_message_str = outbound_message

        system_message = "SYSTEM MESSAGE: Your name is {self.name}, your return address is {self.queue} and this thread is {self.thread}.  Remember:  You must use the 'communicate' tool to respond successfully.  If you do not use the 'communicate' tool, the system will not function properly.  Don't respond with output other than the 'communicate' tool."

        outbound_message_str = f"""
            {outbound_message_str}\n{system_message}
            \n\n
        """

        # Send the message to the agent for processing.  The agent will (hopefully) not return a response
        try:

            self.notify_ui_of_thinking_started()

            # This will block until the response is received
            self.llm.run(
                assistant_id=self.assistant_id, 
                thread_user_message=outbound_message_str, 
                io_handler=self.io_handler
            )

            direct_response = self.llm.get_last_assistant_message()

            self.logger.debug(f"interact() - Direct LLM Response: {direct_response}")

            self.notify_ui_of_thinking_completed()

        except Exception as e:
            self.logger.error(f"interact() - Error calling the llm: {e}")
            time.sleep(1)
            # self.interact(f"There was an error when calling the llm (you): {e}.  Please let the user know.  {system_message}.")