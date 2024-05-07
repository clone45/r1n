import chromadb
from pathlib import Path

class chromaDBClientDeleteCollection():

    def __init__(self, arguments):
        self.arguments = arguments

    @staticmethod
    def get_definition():
        return {
            "name": "chromaDBClientDeleteCollection",
            "description": "Delete a collection in a ChromaDB database.",
            "parameters": {
                "type": "object",
                "properties": {
                    "collection_name": {
                        "type": "string",
                        "description": "The name of the collection to delete."
                    },
                },
                "required": ["collection_name"]
            }           
        }

    def run(self, io_handler=None):

        path = Path("./storage/chromaDB/data")
        path.mkdir(parents=True, exist_ok=True)

        # Initialize ChromaDB client
        client = chromadb.PersistentClient(path=str(path))

        # Create a collection
        collection_name = self.arguments['collection_name']
        client.delete_collection(collection_name)