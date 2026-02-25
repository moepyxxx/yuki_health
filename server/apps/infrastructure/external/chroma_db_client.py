import chromadb
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from .vector_db_client import VectorDBClient

from typing import Any


class ChromaDBClientError(Exception):
    """ChromaDBClientError"""


class ChromaDBClient(VectorDBClient):
    def __init__(self):
        super().__init__()

        self.client = chromadb.HttpClient(host="localhost", port=8001)
        self.embeddings_model = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001"
        )

    def add(
        self,
        collection_name: str,
        document: str,
        id: str,
        metadata: Any,
    ) -> None:
        collection = self.client.get_or_create_collection(name=collection_name)

        try:
            collection.add(
                documents=[document],
                ids=[id],
                metadatas=[metadata],
                embeddings=[self.embeddings_model.embed_query(document)],
            )
        except Exception as e:
            raise ChromaDBClientError(f"Failed to add document: {e}")

    def query(
        self,
        collection_name: str,
        query: str,
        n_results: int = 5,
    ) -> Any:
        try:
            collection = self.client.get_collection(name=collection_name)
        except Exception:
            raise ChromaDBClientError(f"Collection {collection_name} does not exist.")

        try:
            query_vector = self.embeddings_model.embed_query(query)
        except Exception as e:
            raise ChromaDBClientError(f"Failed to embed query: {e}")

        return collection.query(query_embeddings=[query_vector], n_results=n_results)
