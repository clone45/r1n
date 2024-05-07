import chromadb

from pathlib import Path

class chromaDBClientListCollections():

    def __init__(self, arguments):
        self.arguments = arguments

    @staticmethod
    def get_definition():
        return {
            "name": "chromaDBClientListCollections",
            "description": "List all collections in a ChromaDB database.",
            "parameters": {}
        }

    def run(self, io_handler=None):

        # Initialize ChromaDB client
        path = Path("./storage/chromaDB/data")
        path.mkdir(parents=True, exist_ok=True)

        # Initialize ChromaDB client
        client = chromadb.PersistentClient(path=str(path))

        # List all collections
        collections = client.list_collections()

        # Format the list of collections for output
        collection_names = [collection.name for collection in collections]

        return {"collections": collection_names}
