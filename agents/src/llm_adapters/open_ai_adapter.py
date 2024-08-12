import openai
import os
import json
import time
import logging
from src.logging.logging_config import setup_papertrail_logging
from src.tools.tool_manager import ToolManager
from dotenv import load_dotenv
from src.llm_adapters.llm_adapter import LLMAdapter

class OpenAIAdapter(LLMAdapter):
    def __init__(self, thread_id=None):
        
        load_dotenv()
        
        # Prepare and configure Papertrail logging
        setup_papertrail_logging('open_ai_adapter')
        self.logger = logging.getLogger('open_ai_adapter')

        self.api_key = os.getenv('OPEN_AI_KEY')
        if not self.api_key:
            raise ValueError("OpenAI key not found. Please check your .env file.")

        self.client = openai.OpenAI(api_key=self.api_key)
        self.tools = ToolManager.get_instance()

        if thread_id:
            self.thread = self.client.beta.threads.retrieve(thread_id)
        else:
            self.thread = self.client.beta.threads.create()
            
        self.thread_id = self.thread.id

        self.logger.info(f"Thread ID: {self.thread_id}")

    def list_assistants(self):
        return self.client.beta.assistants.list()

#    def create_assistant(self, assistant_config):
#        try:
#            return self.client.beta.assistants.create(**assistant_config)
#        except Exception as e:
#            self.logger.error(f"An error occurred while creating an assistant.  This may occur if Open AI's APIs are temporarily down, or if there are network connection issues. The exception is: {e}")
#            return None
        
    def update_assistant(self, assistant_id, assistant_config):
        return self.client.beta.assistants.update(assistant_id, **assistant_config)

    def delete_assistant(self, assistant_id):
        return self.client.beta.assistants.delete(assistant_id)

    def create_thread_message(self, role, content):
        return self.client.beta.threads.messages.create(
            thread_id=self.thread_id,
            role=role,
            content=content
        )

    def _create_run(self, assistant_id, instructions=None):
        params = {
            "thread_id": self.thread_id,
            "assistant_id": assistant_id,
            "instructions": instructions
        }
        return self.client.beta.threads.runs.create(**params)

    def retrieve_run(self, run_id):
        return self.client.beta.threads.runs.retrieve(thread_id=self.thread_id, run_id=run_id)

    def submit_tool_outputs(self, run_id, tool_outputs):
        try:
            return self.client.beta.threads.runs.submit_tool_outputs(
                thread_id=self.thread_id,
                run_id=run_id,
                tool_outputs=tool_outputs
            )
        except Exception as e:
            self.logger.error(f"An error occurred while submitting tool outputs: {e}")
            return None
    
    def get_vector_store(self, vector_store_id):
        try:
            vector_store = self.client.beta.vector_stores.retrieve(vector_store_id)
            return vector_store
        except Exception as e:
            return None
    
    def create_vector_store(self, vector_store_config):
        return self.client.beta.vector_stores.create(**vector_store_config)

    def attach_vector_store_to_assistant(self, assistant_id, vector_store_id):
        self.client.beta.assistants.update(
            assistant_id=assistant_id,
            tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
        )

    def upload_and_poll(self, vector_store_id, file_streams):
        return self.client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store_id, 
            files=file_streams
        )
    

    # Fetch all of the messages in a thread
    def list_messages(self):
        return self.client.beta.threads.messages.list(thread_id=self.thread_id)
    
    def get_last_assistant_message(self):
        messages = self.list_messages()
        for message in messages.data:
            if message.role == 'assistant':
                if hasattr(message, 'content') and len(message.content) > 0 and hasattr(message.content[0], 'text') and hasattr(message.content[0].text, 'value'):
                    return message.content[0].text.value
        return None
    

    def call_tools(self, tool_calls, io_handler=None):

        print(f"tool_calls: {tool_calls}")

        tool_outputs = []
        for tool_call in tool_calls:
            
            tool_name = tool_call.function.name

            try:
                tool_class = self.tools.get_tool_class(tool_name)  # Use ToolManager instance to get the tool class
                tool_instance = tool_class(json.loads(tool_call.function.arguments))

                # run the tool and get the response
                function_response = tool_instance.run(io_handler)
                tool_output = {"tool_call_id": tool_call.id, "output": json.dumps(function_response)}
                tool_outputs.append(tool_output)

                print(f"Tool output: {tool_output}")
                
            except Exception as e:

                # If an error occurs, log the error and return an error message
                error_message = str(e)
                self.logger.error(f"Error executing tool {tool_name}: {error_message}")
                tool_outputs.append({"tool_call_id": tool_call.id, "output": json.dumps({"status": "error", "message": error_message})})

        return tool_outputs

    
    def list_thread_messages(self):
        try:
            response = self.client.beta.threads.messages.list(thread_id=self.thread_id)
            return response
        except Exception as e:
            self.logger.error(f"An error occurred while retrieving thread messages: {e}")
            return []


    #
    # run() method that uses async/await to handle the OpenAI API calls
    #
    # Written by Roccha (https://community.openai.com/u/roccha/summary)
    # https://community.openai.com/t/create-and-poll-with-function-calling/727672/8?u=clone45
    # with very minor adaptations by Bret and ChatGPT
    #
    def run(self, assistant_id, thread_user_message, instructions=None, io_handler=None):
        
        # Create a message in the thread
        self.client.beta.threads.messages.create(
            thread_id=self.thread_id,
            role="user",
            content=thread_user_message
        )

        # Create and start a run, polling automatically
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread_id,
            assistant_id=assistant_id,
            instructions=instructions,
            # tool_choice={"type": "function", "function": {"name": "communicate"}}
        )

        while True:
            time.sleep(2)
            run = self.client.beta.threads.runs.retrieve(thread_id=self.thread_id, run_id=run.id)
            print(f"Run status: {run.status}")

            # Handle run statuses
            if run.status == 'requires_action':
                # Handle function calls
                tool_outputs = self.call_tools(run.required_action.submit_tool_outputs.tool_calls, io_handler)
                self.client.beta.threads.runs.submit_tool_outputs(
                    thread_id=self.thread_id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )

            # RUN STATUS: COMPLETED
            elif run.status == "completed":
                # response_message = self.get_response(self.thread_id)
                response_message = self.get_last_assistant_message()
                return {"response": response_message, "status_code": 200}
            
            # RUN STATUS: EXPIRED | FAILED | CANCELLED | INCOMPLETE
            elif run.status in ['expired', 'failed', 'cancelled', 'incomplete']:
                error_details = run.last_error.message if run.last_error else 'No error details'
                return {"response": error_details, "status_code": 500}




