
import chromadb

from app.services.embedding_service import create_embedding


# -------------------------
# Vector database
# -------------------------

client = chromadb.PersistentClient(
    path="storage/chroma"
)

collection = client.get_or_create_collection(
    name="document_chunks"
)


# -------------------------
# Salva un chunk
# -------------------------

def add_chunk(
    document_id: str,
    chunk_id: str,
    text: str,
):
    """
    Crea l'embedding di un chunk
    e lo salva nel vector database.
    """

    embedding = create_embedding(text)

    collection.add(
        ids=[chunk_id],
        embeddings=[embedding],
        documents=[text],
        metadatas=[
            {
                "document_id": document_id
            }
        ]
    )


# -------------------------
# Cerca chunk simili
# -------------------------

def search_similar_chunks(
    document_id: str,
    query: str,
    n_results: int = 3,
):
    """
    Cerca i chunk semanticamente più vicini
    alla domanda all'interno di un documento.
    """

    query_embedding = create_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where={
            "document_id": document_id
        }
    )

    return results
