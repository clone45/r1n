import abc

class LLMAdapter:

    def list_assistants(self):
        pass

    def create_assistant(self, assistant_config):
        pass

    def delete_assistant(self, assistant_id):
        pass

    def create_thread_message(self, role, content):
        pass

    def retrieve_run(self, run_id):
        pass

    def submit_tool_outputs(self, run_id, tool_outputs):
        pass

    def run(self, 
            assistant_id, 
            thread_user_message, 
            instructions=None, 
            io_handler=None):
        pass