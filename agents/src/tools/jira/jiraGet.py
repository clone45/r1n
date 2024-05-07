

import os
import json
import requests
import logging
from dotenv import load_dotenv

class jiraGet():
    def __init__(self, arguments):
        self.arguments = arguments
        load_dotenv()  # Load environment variables

    @staticmethod
    def get_definition():
        return {
            "name": "jiraGet",
            "description": "Perform a GET request to Jira API and return the results",
            "parameters": {
                "type": "object",
                "properties": {
                    "resource": {
                        "type": "string",
                        "description": "The Jira API resource path"
                    },
                    "query_params": {
                        "type": "object",
                        "description": "Query parameters for the GET request",
                        "additionalProperties": True
                    }
                },
                "required": ["resource"]
            }
        }

    def run(self, io_handler=None):
        resource = self.arguments['resource']
        query_params = self.arguments.get('query_params', {})

        jira_server = os.getenv('JIRA_SERVER')
        jira_username = os.getenv('JIRA_USERNAME')
        jira_api_token = os.getenv('JIRA_API_TOKEN')

        url = f"{jira_server}/rest/api/3/{resource}"
        auth = (jira_username, jira_api_token)

        try:
            response = requests.get(url, params=query_params, auth=auth)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"__Error in runJiraGet: {str(e)}")
            return {"error": str(e)}
