# This tool does do the following:
# 1. It clears out the active_agents table in the database.
# 2. It broadcasts a message to all running agents using the RabbitMQIOHandler instance (io_handler) that's passing into the constructor.
# 3. It waits for a response from each agent for a specified amount of time.  Maybe 2 seconds.
# 4. It reads the database to see which agents have responded.
# 5. It returns a list of agents that have responded.

import json
import time
from src.repositories.PresenseRepository import PresenceRepository

class discoverTeamMembers():

    def __init__(self, *args, **kwargs):
        self.agent_repository = PresenceRepository()

    @staticmethod
    def get_definition():
        return {
            "name": "discoverTeamMembers",
            "description": "Discover all AI agents that are currently active. If you're asked to do something that you can't do, you may want to use this tool to find out if any other agents can help out.",
            "parameters": {
                # No parameters required for discovering team members
            }
        }

    def run(self, io_handler=None):
        # Clear all agents from the database
        try:
            # self._agent_presence_manager.clear_all_agents()
            self.agent_repository.delete_all()
        except Exception as e:
            return f"Error clearing agents from database: {str(e)}"

       # Read the database to see which agents have responded
        try:
            # Broadcast a message to all agents
            io_handler.broadcast_message("broadcast_queue", "system.register_presence", "")
            
            # Instead of sleeping for 3 seconds, consider using the  RabbitMQ Management HTTP API to list all queues and 
            # their details

            # Wait for responses
            time.sleep(3)
 
            agents = self.agent_repository.list_all()
            agents_json = json.dumps(agents)

            result = {"status": "success", "content": agents_json}

            return json.dumps(result)

        except Exception as e:
            print(f"Error sending message: {e}")
            result = {"status": "error", "content": str(e)}

       