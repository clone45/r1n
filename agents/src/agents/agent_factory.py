# agent_factory.py
from .open_ai_agent import OpenAIAgent
from .ollama_agent import OllamaAgent
from src.llm_adapters.open_ai_adapter import OpenAIAdapter
from src.llm_adapters.ollama_adapter import OllamaAdapter
# from dotenv import load_dotenv

class AgentFactory:

    def __init__(self):

        # load_dotenv()

        self.agent_class_map = {
            "gpt-4-1106-preview": {
                "agent_class": OpenAIAgent, 
                "llm_class": OpenAIAdapter
            },
            "gpt-4-turbo": {
                "agent_class": OpenAIAgent, 
                "llm_class": OpenAIAdapter
            },
            "ollama": {
                "agent_class": OllamaAgent, 
                "llm_class": OllamaAdapter
            },
            # Add other models and corresponding agent and llm classes here
            # TODO: Move this to the database
        }

    def create_agent(self, instance_uuid, profile, role, reset_assistant, thread, io_handler):

        llm_model = role.get('model', 'gpt-4-1106-preview')
        model_config = self.agent_class_map.get(llm_model)

        if model_config:

            # Instantiate the LLM adapter
            llm = model_config["llm_class"](thread)

            # Get the agent class name
            agent_class = model_config["agent_class"]

            # Create the agent instance and return it
            return agent_class(instance_uuid, profile, llm, role, reset_assistant, thread, io_handler)
        
        else:
            raise ValueError(f"Can't locate llm associated with model in agent_class_map: {llm_model}")