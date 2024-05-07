
import os
import subprocess
import json
import uuid
import logging
from dotenv import load_dotenv
from pathlib import Path

class agentSpawn():

    def __init__(self, arguments):
        self.arguments = arguments

    @staticmethod
    def get_definition():
        pid = os.getpid()
        return {
            "name": "agentSpawn",
            "description": """
                This function provides a way to spawn a new agent.  
                This is especially useful when you need to spawn a new agent to handle a specific task, 
                  or if you want to make updates to the codebase and use another agent to test it out. 
                Agents can be stopped by sending them a single 'quit' statement on the message bus. 
                If you don't provide a folder name, the default agent will be used.  To check what agent folders are available, you can use the agentsList tool.
                If you want to reset the agent, you can set the reset parameter to True.  This will re-register the agent with the LLM.  
                Typically, you will only want to reset an agent if you are changing the definition of an agent.  If you don't need this, don't provide it.
            """,
            "parameters": {
                "type": "object",
                "properties": {
                    "role_folder": {
                        "type": "string",
                        "description": "The folder name containing the role information.  If you don't provide a folder name, the default agent will be used.  If you're not sure what agent to spawn, you can use the agentsList tool."
                    },
                    "reset": {
                        "type": "boolean",
                        "description": "If you want to reset the agent, you can set this to True.  This will re-register the agent with the LLM.  Typically, you will want to do this if you are changing the definition of an agent.  If you don't need this, don't provide it."     
                    },
                    "name": {
                        "type": "string",
                        "description": "The name of the agent.  If you were asked to spawn an agent, but weren't provided a name, please make one up.  It should be a common, unique first name (Like Joe, Mellisa, Dmitri, Lucas, Midori, etc.) in the language of your choice."
                    },
                    "thread": {
                        "type": "string",
                        "description": "The thread is an id that's associated with the agent's conversation.  If you don't provide this, a new thread will be created.  Leave it blank unless you specifically want to use a thread that's already been created.  Here's how OpenAI puts it: Assistants can access persistent Threads. Threads simplify AI application development by storing message history and truncating it when the conversation gets too long for the model’s context length."
                    },
                },
                "required": ["role_folder"]
            }
        }

    def run(self, io_handler=None):

        load_dotenv()

        role_folder = self.arguments.get('role_folder', 'default')
        agent_name = self.arguments.get('name', '')
        reset = self.arguments.get('reset') if self.arguments.get('reset') else False
        instance_uuid = str(uuid.uuid4())

        roles_path = Path(os.getenv('CONFIG_DIR') + '/roles')

        current_path = Path(__file__).resolve()
        roles_folder_path = current_path.parents[3] / roles_path

        # check if the agents folder exists
        if not os.path.isdir(roles_folder_path):
            error_message = f"__Agents folder '{roles_folder_path}' does not exist.  Please convey this information to the user."
            logging.error(error_message)
            return json.dumps({"status": "error", "message": error_message})

        # Before starting the agent, we need to check if the agent folder exists
        if not os.path.isdir(f"{roles_folder_path}/{role_folder}"):

            # Collect a comma delimited list of available role folders
            role_folders = [name for name in os.listdir(roles_folder_path) if os.path.isdir(f"{roles_folder_path}/{name}")]

            # log the error message
            error_message = f"__Agent folder '{role_folder}' does not exist. Available role folders: {', '.join(role_folders)}.  The path to the agents folder is: {roles_folder_path}.  Please convey this information to the user."
            logging.error(error_message)

            # Return an error message if the agent folder does not exist
            return json.dumps({"status": "error", "message": error_message})

        # Construct the command to run the agent
        # TODO: This is incorrect
        command = ["python", "run.py", "--agent_folder", role_folder, "--instance_uuid", instance_uuid]
        if reset:
            command.append("--reset")
        if agent_name:
            command.append("--name")
            command.append(agent_name)

        try:
            
            # Start the agent in a new background process
            subprocess.Popen(command)

            queue = f"queue_{instance_uuid}"

            # You can log or return some information here if needed
            return json.dumps({"status": "success", "message": f"Agent started listening on queue '{queue}'"})
        except Exception as e:

            # create an error message that includes the exception, the command that was run, and the agents folder path
            error_message = f"An error occurred while trying to start the agent.  The command that was run was: {command}.  The agents folder path is: {agents_folder_path}.  The exception that was raised is: {str(e)}"

            return json.dumps({"status": "error", "message":error_message})