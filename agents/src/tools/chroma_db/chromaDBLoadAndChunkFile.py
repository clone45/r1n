import chromadb
import os
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings

from pathlib import Path
import json
import uuid
from dotenv import load_dotenv

class chromaDBLoadAndChunkFile():

    def __init__(self, arguments):
        self.arguments = arguments

    @staticmethod
    def get_definition():
        return {
            "name": "chromaDBLoadAndChunkFile",
            "description": "Load a file, chunk it, and add each chunk to ChromaDB.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path of the file to load relative to ./storage."
                    },
                    "collection_name": {
                        "type": "string",
                        "description": "The name of the ChromaDB collection to add the chunks to."
                    }
                },
                "required": ["file_path", "collection_name"]
            }
        }

    def run(self, io_handler=None):
        file_path = self.arguments['file_path']
        collection_name = self.arguments['collection_name']

        # Initialize ChromaDB client
        client = chromadb.PersistentClient(path=str(Path("./storage/chromaDB/data")))

        # Define or get the collection
        collection = client.get_or_create_collection(collection_name)

        # Load and process the file
        load_dotenv()

        # Load and process the file
        openai_api_key = os.getenv('OPEN_AI_KEY')  # Load API key from environment

        # Read the file
        file_full_path = os.path.join("./storage", file_path)
        with open(file_full_path, encoding="utf-8") as f:
            file_content = f.read()

        # Chunk the text using OpenAIEmbeddings with API key
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        text_splitter = SemanticChunker(embeddings)
        docs = text_splitter.create_documents([file_content])

        # Add chunks to the collection with metadata
        for i, doc in enumerate(docs):
            metadata = {
                "source": file_path,
                "length": len(doc.page_content),
                "sequence_number": i + 1
            }
            collection.add(
                documents=[doc.page_content],
                metadatas=[metadata],
                ids=[str(uuid.uuid4())]
            )

        return json.dumps({"status": "success", "message": "File loaded, chunked, and added to ChromaDB."})
