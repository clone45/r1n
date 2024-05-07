

from jira import JIRA
import os
import json
import logging
from dotenv import load_dotenv

class jqlQuery():
    def __init__(self, arguments):
        super().__init__(arguments)
        self.arguments = arguments
        load_dotenv()  # Load environment variables

    @staticmethod
    def get_definition():
        return {
            "name": "jqlQuery",
            "description": "Run a JQL query and return the results",
            "parameters": {
                "type": "object",
                "properties": {
                    "jql_query": {
                        "type": "string",
                        "description": "The JQL query string"
                    }
                },
                "required": ["jql_query"]
            }
        }

    def run(self, io_handler=None):
        jql_query = self.arguments['jql_query']
        jira_server = os.getenv('JIRA_SERVER')
        jira_username = os.getenv('JIRA_USERNAME')
        jira_api_token = os.getenv('JIRA_API_TOKEN')

        logging.info(f"__Connecting to Jira")

        try:
            jira = JIRA(server=jira_server, basic_auth=(jira_username, jira_api_token))
        except Exception as e:
            logging.error(f"__Failed to connect to JIRA: {e}")
            return None

        logging.info(f"__Running JQL: {jql_query}")

        try:
            issues = jira.search_issues(jql_query)
            return json.dumps([{"key": issue.key, "summary": issue.fields.summary} for issue in issues])
        except Exception as e:
            try:
                error_message = json.loads(e.text)
                return {"error": error_message["errorMessages"][0]}
            except json.JSONDecodeError:
                return {"error": str(e)}
