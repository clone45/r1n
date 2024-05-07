
import json
import os
from pathlib import Path
from dotenv import load_dotenv
from src.repositories.ProfilesRepository import ProfilesRepository

class agentsList():

    def __init__(self, arguments):
        self.arguments = arguments
        self.profiles_repository = ProfilesRepository()

    @staticmethod
    def get_definition():
        return {
            "name": "agentsList",
            "description": "Scans the agents directory to discover and list all available local agent configurations.  This can be useful if your asked to spawn a new agent by name, or learn more about what agents are available in the system.",
            "parameters": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    def run(self, io_handler=None):

        load_dotenv()

        agents_info = self.profiles_repository.list_all()

        result = {"status": "success", "agents": agents_info}
        return json.dumps(result)