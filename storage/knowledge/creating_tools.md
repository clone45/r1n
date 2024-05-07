## Guide for Creating a New Tool in the Agent Framework

### Introduction
This guide is designed to instruct a Language Learning Model (LLM) on how to create and integrate a new tool into our Agent Framework. A 'tool' in this context is a Python module that performs a specific task or interacts with a particular system or service.

### Prerequisites
- Basic understanding of the structure and operation of our Agent Framework.
- Access to the `tools/` directory in the framework.

### Steps to Create a New Tool

**1. Define the Purpose and Functionality of the Tool**
   - Identify what the tool is intended to do.
   - Define the inputs required and the expected output.

**2. Create a New Python File for the Tool**
   - Navigate to the `tools/` directory.
   - Create a new Python file (`.py`). The name should be descriptive of the tool's functionality.

**3. Import Required Modules**
   ```python
   from src.tools.tool import Tool
   import json
   # Import any other necessary modules.
   ```

**4. Define the Tool Class**
   - The class should inherit from `Tool`.
   - Implement the abstract methods `get_definition()` and `run()`.

   Example:
   ```python
   class MyNewTool(Tool):

       @staticmethod
       def get_definition():
           return {
               "name": "MyNewTool",
               "description": "A brief description of what the tool does.",
               "parameters": {
                   # Define the expected input parameters here
               }
           }

       def run(self, io_handler=None):
           # Tool logic goes here.
           # Process the input and produce the output.
   ```

## Determining Parameters for New Tools

### Understanding Parameters
Parameters are the inputs that your tool will accept. They define what information is necessary for your tool to function properly. When creating a new tool, it's crucial to clearly define its parameters, ensuring they are both sufficient and appropriate for the task at hand.

### Structuring Parameters
- Each tool has a `parameters` field in its definition. This field should be a JSON object describing the expected inputs.
- This object typically contains the following keys:
  - `type`: Always set to `"object"` for a tool.
  - `properties`: An object where each key is a parameter name and the value describes the parameter.
  - `required`: An array of strings listing the names of all required parameters.

### Types of Parameters
- **String**: Used for text-based inputs. Example: `"type": "string"`
- **Boolean**: True or False values. Example: `"type": "boolean"`
- **Integer**: Whole numbers. Example: `"type": "integer"`
- **Array**: A list of values. Specify the type of items in the array. Example: `"type": "array", "items": {"type": "string"}`
- **Object**: A JSON object. Useful for complex inputs. Example: `"type": "object"`

### Deciding on Parameters
1. **Identify the Core Functionality**: Understand precisely what your tool is meant to achieve.
2. **Determine Necessary Inputs**: Based on the functionality, decide what inputs are needed.
3. **Set Required Parameters**: Some inputs might be essential for the tool's operation. Mark these as `required`.
4. **Consider Optional Parameters**: These are parameters that can alter the behavior of the tool but are not essential.
5. **Default Values**: For optional parameters, consider if a default value should be set if the user does not provide one.

### Example Definitions
- **agentSpawn Tool**: Requires `id`, optional `agent_folder`, and `reset` to control behavior.
  - `id` is a unique identifier for the agent.
  - `agent_folder` specifies the directory of the agent.
  - `reset` is a boolean to reset the agent's state.
- **chromaDBCollectionGet Tool**: Requires `ids`, with optional parameters like `where`, `limit`, `offset`, etc., to fetch specific data from ChromaDB.
  - `ids` specify which embeddings to get.
  - `where` and `where_document` are JSON strings for filtering.
  - `limit` and `offset` control the number of results returned.
- **jqlQuery Tool**: Requires a `jql_query` string to execute a JQL query.
  - `jql_query` is the query string used in JIRA.

### Best Practices
- **Clarity**: Ensure each parameter's purpose is clearly defined.
- **Validation**: Consider how you will validate each parameter within your tool.
- **Documentation**: Document each parameter well in your tool's definition for clarity and ease of use.


**5. Handle Input Parameters**
   - Use `self.arguments` within the `run` method to access input parameters.

**6. Implement the Tool Logic**
   - Write the Python code that performs the tool's primary function within the `run` method.

**7. Add Error Handling**
   - Ensure robust error handling within the tool for reliability.

**8. Test the Tool**
   - Create test cases to ensure the tool works as expected.
   - Make use of `tool_runner.py` for isolated testing.

**9. Document the Tool**
   - Add comments and a clear description at the top of the Python file.
   - Include information about input parameters and usage.

**10. Integrate the Tool into the Framework**
   - Ensure the tool is recognized by the `Tools` class.
   - Update any relevant configuration files if necessary.

### Conclusion
After following these steps, the tool will be integrated into the Agent Framework, ready to be utilized by agents. Always ensure the tool is thoroughly tested and documented to maintain the quality and reliability of the framework.
