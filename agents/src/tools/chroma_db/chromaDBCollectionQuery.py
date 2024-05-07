import chromadb
from pathlib import Path

import json

class chromaDBCollectionQuery():

    def __init__(self, arguments):
        self.arguments = arguments

    @staticmethod
    def get_definition():
        return {
            "name": "chromaDBCollectionQuery",
            "description": "Query a ChromaDB collection using embeddings or text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "collection_name": {
                        "type": "string",
                        "description": "The name of the collection to query."
                    },
                    "query_texts": {
                        "type": "string",
                        "description": "The document texts to query. Must be a JSON string of a list of texts."
                    },
                    "query_embeddings": {
                        "type": "string",
                        "description": "The embeddings to query. Must be a JSON string of a list of embeddings."
                    },
                    "n_results": {
                        "type": "integer",
                        "description": "The number of results to return."
                    },
                    "where": {
                        "type": "string",
                        "description": "Filter conditions. Must be a JSON string of a dictionary."
                    }
                },
                "required": ["collection_name", "n_results"]
            }
        }

    def run(self, io_handler=None):

        collection_name = self.arguments['collection_name']
        n_results = self.arguments['n_results']
        where = json.loads(self.arguments['where']) if 'where' in self.arguments else {}
        
        query_texts = json.loads(self.arguments['query_texts']) if 'query_texts' in self.arguments else None
        query_embeddings = json.loads(self.arguments['query_embeddings']) if 'query_embeddings' in self.arguments else None

        # Ensure either query_texts or query_embeddings is provided, not both
        if query_texts and query_embeddings:
            raise ValueError("Provide either query_embeddings or query_texts, not both.")

        path = Path("./storage/chromaDB/data")
        path.mkdir(parents=True, exist_ok=True)

        # Initialize ChromaDB client
        client = chromadb.PersistentClient(path=str(path))

        # Get the collection
        collection = client.get_or_create_collection(collection_name)

        # Perform the query
        results = collection.query(
            query_embeddings=query_embeddings,
            query_texts=query_texts,
            n_results=n_results,
            where=where
        )

        return results
