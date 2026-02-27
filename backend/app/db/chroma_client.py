from chromadb import EphemeralClient, PersistentClient
from chromadb.utils import embedding_functions
from ..config import settings
from typing import Optional


# initialize client and collection
_client: Optional[object] = None
_collection = None


def get_client():
    global _client
    if _client is None:
        # Use PersistentClient for data persistence
        _client = PersistentClient(path="./chroma_db")
    return _client


def get_collection():
    global _collection
    if _collection is None:
        client = get_client()
        try:
            _collection = client.get_collection(name=settings.CHROMA_COLLECTION)
        except Exception as e:
            # Create collection if it doesn't exist
            try:
                _collection = client.create_collection(
                    name=settings.CHROMA_COLLECTION,
                    embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
                        model_name=settings.EMBEDDING_MODEL
                    )
                )
            except Exception:
                # Collection might have been created by another thread, try to get it
                _collection = client.get_collection(name=settings.CHROMA_COLLECTION)
    return _collection
