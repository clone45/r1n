import chromadb

from pathlib import Path

class chromaDBCollectionPeek():

    def __init__(self, arguments):
        self.arguments = arguments

    @staticmethod
    def get_definition():
        return {
            "name": "chromaDBCollectionPeek",
            "description": "Get the first few results from a ChromaDB collection.",
            "parameters": {
                "type": "object",
                "properties": {
                    "collection_name": {
                        "type": "string",
                        "description": "The name of the collection to peek into."
                    },
                    "limit": {
                        "type": "integer",
                        "description": "The number of results to return. Default is 10."
                    }
                },
                "required": ["collection_name"]
            }
        }

    def run(self, io_handler=None):
        collection_name = self.arguments['collection_name']
        limit = self.arguments.get('limit', 10)  # Default limit is 10 if not specified

        path = Path("./storage/chromaDB/data")
        path.mkdir(parents=True, exist_ok=True)

        # Initialize ChromaDB client
        client = chromadb.PersistentClient(path=str(path))

        # Get the collection
        collection = client.get_or_create_collection(collection_name)

        # Peek into the collection
        results = collection.peek(limit=limit)

        return results
