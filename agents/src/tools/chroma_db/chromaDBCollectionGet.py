import chromadb
from pathlib import Path

import json

class chromaDBCollectionGet():

    def __init__(self, arguments):
        self.arguments = arguments

    @staticmethod
    def get_definition():
        return {
            "name": "chromaDBCollectionGet",
            "description": "Get embeddings and their associated data from ChromaDB.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ids": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "The ids of the embeddings to get. Optional."
                    },
                    "where": {
                        "type": "string",
                        "description": "A JSON string representing a Where type dict to filter results by. Optional."
                    },
                    "limit": {
                        "type": "integer",
                        "description": "The number of documents to return. Optional."
                    },
                    "offset": {
                        "type": "integer",
                        "description": "The offset to start returning results from. Optional."
                    },
                    "where_document": {
                        "type": "string",
                        "description": "A JSON string representing a WhereDocument type dict to filter by the documents. Optional."
                    },
                    "include": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "A list of what to include in the results. Optional."
                    }
                },
                "required": ["ids"]
            }
        }

    def run(self, io_handler=None):
        ids = self.arguments.get('ids')
        where = json.loads(self.arguments['where']) if 'where' in self.arguments else None
        limit = self.arguments.get('limit')
        offset = self.arguments.get('offset')
        where_document = json.loads(self.arguments['where_document']) if 'where_document' in self.arguments else None
        include = self.arguments.get('include', ["metadatas", "documents"])

        path = Path("./storage/chromaDB/data")
        path.mkdir(parents=True, exist_ok=True)

        # Initialize ChromaDB client
        client = chromadb.PersistentClient(path=str(path))

        # Get results
        results = client.get(
            ids=ids,
            where=where,
            limit=limit,
            offset=offset,
            where_document=where_document,
            include=include
        )

        return results