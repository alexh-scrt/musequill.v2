import chromadb
from chromadb.config import Settings
import logging

logger = logging.getLogger(__name__)

def clear_and_recreate_collection(chroma_host: str, chroma_port: int, collection_name: str):
    """
    Clear existing ChromaDB collection and recreate it for new embedding dimensions.
    
    Args:
        chroma_host: ChromaDB host
        chroma_port: ChromaDB port  
        collection_name: Name of the collection to recreate
    """
    try:
        # Initialize Chroma client
        chroma_client = chromadb.HttpClient(
            host=chroma_host,
            port=chroma_port,
            settings=Settings(
                chroma_server_authn_credentials=None,
                chroma_server_authn_provider=None
            )
        )
        
        # Try to delete existing collection
        try:
            chroma_client.delete_collection(name=collection_name)
            logger.info(f"Deleted existing collection: {collection_name}")
        except Exception as e:
            logger.info(f"Collection {collection_name} doesn't exist or couldn't be deleted: {e}")
        
        # Create new collection with metadata for the new embedding model
        new_collection = chroma_client.create_collection(
            name=collection_name,
            metadata={
                "description": "Research materials for book writing",
                "embedding_model": "nomic-embed-text",  # 768 dimensions
                "embedding_dimensions": 768,
                "created_at": "2025-08-01T00:00:00Z"
            }
        )
        
        logger.info(f"Created new collection '{collection_name}' for nomic-embed-text (768 dimensions)")
        return new_collection
        
    except Exception as e:
        logger.error(f"Error recreating collection: {e}")
        raise

# Example usage:
if __name__ == "__main__":
    # Replace with your actual configuration values
    CHROMA_HOST = "localhost"  # or your chroma host
    CHROMA_PORT = 18000        # or your chroma port
    COLLECTION_NAME = "research_collection"  # or your collection name
    
    clear_and_recreate_collection(CHROMA_HOST, CHROMA_PORT, COLLECTION_NAME)