import ollama
from src.tools.tool_manager import ToolManager
from src.llm_adapters.llm_adapter import LLMAdapter
import json

class OllamaAdapter(LLMAdapter):
    def __init__(self, thread_id=None):
        pass

    def run(self, 
        content=None, 
        instructions=None, 
        io_handler=None):

        print("Content: ", content)

        response = ollama.chat(model='mistral', messages=[
            {
                'role': 'user',
                'content': content
            }
        ])

        print("Response: ", response)

        return(response)

        # Somehow pull the tool calls from the response
        # then call the tools
        # should I then send the tool output back into the model, like I do with the OpenAIAdapter?
        # Also, whatever is calling this will need to 
        # return response['message']['content']

