# tool_manager.py

import os
import importlib.util
import logging
from dotenv import load_dotenv
from pathlib import Path
import sys

class ToolManager:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ToolManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        
        load_dotenv()
        
        current_path = os.path.dirname(os.path.realpath(__file__))

        # use current path to find the tools directory
        self.tools_root = os.path.join(current_path)

        # Check if the tools directory exists
        if not os.path.exists(self.tools_root):
            raise FileNotFoundError(f"Tools directory not found at path: {self.tools_root}")
        else:
            logging.info(f"__Tools root is: {self.tools_root}")

        if not hasattr(self, '_initialized'): 
            self.tool_path_map = self._load_tools()
            self._initialized = True

    #
    # _load_tools
    #
    # The _load_tools method is designed to dynamically discover and map Python files as tools within
    # a specified directory structure. It scans through a root directory (named 'tools' in this case) 
    # and its subdirectories to find Python files (those ending with .py, excluding __init__.py). 
    # For each of these Python files, it extracts the file name (minus the .py extension) as the 
    # tool's name and calculates the file's relative path from the root directory. This information 
    # is stored in a dictionary, where each tool's name is a key, and its relative path is the value. 
    # 
    # The purpose of this method is to create a mapping of tool names to their respective file paths, 
    # facilitating the dynamic loading and management of these tools elsewhere in the application.

    def _load_tools(self):

        # Initialize an empty dictionary to store the mapping of tool names to their paths.
        tool_path_map = {}

        # Use os.walk to iterate through the directory tree of the 'tools' directory.
        # 'root' is the current directory path, 'dirs' is the list of subdirectories, and 'files' is the list of files in 'root'.

        for root, dirs, files in os.walk(self.tools_root):
            for file in files:

                # Check if the file is a Python file (ends with '.py') and is not '__init__.py'.
                if file.endswith('.py') and file != '__init__.py':
                    
                    # Extract the tool name from the file name by removing the '.py' extension.
                    tool_name = file[:-3]
                    
                    # Compute the relative path of the file from the tools_root. This is the path from 'tools' to the tool file.
                    relative_path = os.path.relpath(os.path.join(root, file), self.tools_root)
                    
                    # Map the tool name to its relative path in the tool_path_map dictionary.
                    tool_path_map[tool_name] = relative_path
                    
        # Log the tool path map for debugging purposes.
        # logging.debug(f"__Tool path map: {tool_path_map}")

        # Return the dictionary containing the mappings of tool names to their paths.
        return tool_path_map

    def load_tools(self, tool_names):

        tool_definitions = []
        for tool in tool_names:

            if isinstance(tool, str):

                # Check if the tool name is a directory path and expand it to include all tools in the directory.
                expanded_tool_names = self._convert_tool_path_to_tool_names(tool)

                for expanded_tool_name in expanded_tool_names:
                    # logging.info(f"__Loading tool {expanded_tool_name}")
                    try:
                        tool_class = self.get_tool_class(expanded_tool_name)  # Use Tools instance to get the tool class
                        tool_definitions.append({"type": "function", "function": tool_class.get_definition()})
                    except (ImportError, AttributeError) as e:
                        logging.error(f"__Error loading tool {expanded_tool_name}: {e}")

            # Handle special cases such as {"type": "file_search"}
            elif isinstance(tool, dict) and 'type' in tool:
                tool_definitions.append(tool)

            else:
                logging.error(f"__Invalid tool definition: {tool}")

        # logging.info(f"__tool_definitions: {tool_definitions}")
        return tool_definitions

    
    def load_module_from_path(self, module_name, file_path):
        """Load a module from a given file path.

        Args:
            module_name (str): Name you want to assign to the module.
            file_path (str): Full path to the .py file containing the module.

        Returns:
            Module: The loaded module.
        """
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None:
            raise ImportError(f"Could not load spec from {file_path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        # Optionally add the module to sys.modules
        sys.modules[module_name] = module
        return module


    #
    # get_tool_class
    #
    # The get_tool_class method is a part of the Tools class. It's used to dynamically 
    # load a Python class from a file based on a given tool name. This method first checks 
    # if the tool name exists in the tool_path_map, a dictionary that maps tool names to 
    # their file paths. If found, it constructs the full file path to the tool's Python file.
    # It then uses importlib, a Python standard library for handling module import operations, 
    # to dynamically load the module from the constructed path. Once loaded, it retrieves the 
    # tool class from the module. The tool class name is expected to be the same as the tool 
    # name. Finally, the method checks if the retrieved class is a subclass of the Tool class, 
    # ensuring it is the correct type of tool class. If it is, the method returns this tool class.
    # 
    # This approach allows the program to flexibly and dynamically load tool classes, enabling 
    # easy management of tools without hardcoding their paths or names into the application's code.

    def get_tool_class(self, tool_name):
        # Check if the tool name exists in the tool path map dictionary.
        if tool_name in self.tool_path_map:
            
            tool_path = self.tool_path_map[tool_name]
            tool_full_path = os.path.join(self.tools_root, tool_path)

            try:
                # tool_module = importlib.import_module(tool_full_path)
                tool_module = self.load_module_from_path(tool_name, tool_full_path)
            except ModuleNotFoundError as e:
                logging.error(f"__Error importing tool module {e}")
                logging.error(f"__ - Tool name is: {tool_name}")
                logging.error(f"__ - Tool full path is: {tool_full_path}")
                logging.error(f"__ - Current working directory is: {os.getcwd()}")
                return None
            
            try:
                tool_class = getattr(tool_module, tool_name)
                return tool_class
            except AttributeError as e:
                logging.error(f"__Error loading tool {e}")
                logging.error(f"__ - Tool name is: {tool_name}")
                logging.error(f"__ - Tool path is: {tool_path}")
                logging.error(f"__ - Current working directory is: {os.getcwd()}")
                return None

        else:
            raise ImportError(f"__Tool {tool_name} not found in tool path map. Path map: {self.tool_path_map}")



    # Users can either specify a tool name such as "fileSystemCheckExists", or they can specify 
    # a path to a tool folder, such as "file_system".  If a tool folder is specified, then we
    # need to iterate through the folder recursively and replace the folder name in the tools_strings
    # list with the tool names.
    
    def _convert_tool_path_to_tool_names(self, tool_string):
        base_path = f"{self.tools_root}/"  # Base path of the tools directory

        if tool_string.startswith('/'):
            folder_path = os.path.join(base_path, tool_string[1:])  # Construct the full path

            # Check if the path exists and is a directory
            if os.path.exists(folder_path) and os.path.isdir(folder_path):
                tool_names = []
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        if file.endswith('.py') and not file.startswith('__'):
                            tool_name = os.path.splitext(file)[0]
                            tool_names.append(tool_name)
                return tool_names
            else:
                logging.error(f"__Warning: Tool path {folder_path} does not exist or is not a directory. Tools root is {self.tools_root}")
                return []
        else:
            return [tool_string]

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance