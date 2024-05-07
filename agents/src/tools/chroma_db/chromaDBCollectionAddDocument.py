import chromadb

from pathlib import Path
import uuid
import json

class chromaDBCollectionAddDocument():

    def __init__(self, arguments):
        self.arguments = arguments

    @staticmethod
    def get_definition():
        return {
            "name": "chromaDBCollectionAddDocument",
            "description": "Add a document to a ChromaDB collection.",
            "parameters": {
                "type": "object",
                "properties": {
                    "document": {
                        "type": "string",
                        "description": "The document (text) to add"
                    },
                    "collection_name": {
                        "type": "string",
                        "description": "The name of the collection to add the document to."
                    },
                    "metadatas": {
                        "type": "string",
                        "description": "Metadata to add to the document.  Example metadata: [{'category': 'animal'}]"
                    },
                },
                "required": ["document", "collection_name", "metadatas"]
            }
        }

    def run(self, io_handler=None):
        
        document = self.arguments['document']
        collection_name = self.arguments['collection_name']
        metadata = json.loads(self.arguments['metadatas'])

        path = Path("./storage/chromaDB/data")
        path.mkdir(parents=True, exist_ok=True)

        # Initialize ChromaDB client
        client = chromadb.PersistentClient(path=str(path))

        # Define or get the collection
        collection = client.get_or_create_collection(collection_name)

        # add the documents in the db.  Use a uuid for the id.
        collection.add(
            documents=[document],
            metadatas=metadata,
            ids=[str(uuid.uuid4())]
        )
