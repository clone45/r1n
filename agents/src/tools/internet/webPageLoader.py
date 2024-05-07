
import requests
from bs4 import BeautifulSoup
import json
import logging

class webPageLoader():

    def __init__(self, arguments):
        self.arguments = arguments

    @staticmethod
    def get_definition():
        return {
            "name": "webPageLoader",
            "description": "Load the contents of a specific webpage",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL of the webpage to load"
                    }
                },
                "required": ["url"]
            }
        }

    def run(self, io_handler=None):
        url = self.arguments['url']
        try:
            response = requests.get(url)
            response.raise_for_status()

            # Use BeautifulSoup to parse and extract text
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text(separator=' ', strip=True)

            return json.dumps({"status": "success", "response": text})
            
        except Exception as e:
            logging.error(f"__Error in webPageFetcher tool: {str(e)}")
            return json.dumps({"status": "error", "message": str(e)})
