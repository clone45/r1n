import importlib
import json

from src.tools import Tools
import os

class toolReloader():
    @staticmethod
    def get_definition():
        return {
            "name": "toolReloader",
            "description": "Reloads a specified tool to update its logic on-the-fly.",
            "parameters": {
                "type": "object",
                "properties": {
                    "tool_name": {
                        "type": "string",
                        "description": "The name of the tool to be reloaded."
                    }
                },
                "required": ["tool_name"]
            }
        }

    def run(self, io_handler=None):
        tools_instance = Tools.get_instance()
        tool_name = self.arguments.get('tool_name')

        try:
            if tool_name in tools_instance.tool_path_map:
                tool_path = os.path.join('tools', tools_instance.tool_path_map[tool_name])
                # Convert file system path to Python module path (replace backslashes with dots and remove .py)
                tool_module_name = tool_path.replace(os.sep, '.').replace('.py', '')

                # Use import_module to load the module
                tool_module = importlib.import_module(tool_module_name)
                # Reload the module
                importlib.reload(tool_module)

                return json.dumps({"status": "success", "message": f"Tool {tool_name} reloaded successfully."})
            else:
                return json.dumps({"status": "error", "message": f"Tool {tool_name} not found."})
        except Exception as e:
            return json.dumps({"status": "error", "message": f"Error reloading tool {tool_name}: {e}"})
