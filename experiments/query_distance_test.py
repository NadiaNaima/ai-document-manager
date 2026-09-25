from app.services.embedding_service import create_embedding
from app.services.vector_store import collection


CHUNK_ID = "test-real-pdf-chunk-10"


queries = [
    "Quali mezzi di sussistenza sono richiesti?",
    "Quali sono i mezzi di sussistenza?",
    "Quali risorse economiche sono necessarie?",
    "Quali sono i requisiti economici per il soggiorno?",
]


result = collection.get(
    ids=[CHUNK_ID],
    include=["documents", "embeddings"],
)


chunk_text = result["documents"][0]
chunk_embedding = result["embeddings"][0]


def cosine_distance(vector_a, vector_b):

    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    norm_a = sum(
        a * a
        for a in vector_a
    ) ** 0.5

    norm_b = sum(
        b * b
        for b in vector_b
    ) ** 0.5

    cosine_similarity = (
        dot_product
        / (norm_a * norm_b)
    )

    return 1 - cosine_similarity


print()
print("=" * 80)
print("QUERY DISTANCE TEST")
print("=" * 80)

print()
print("CHUNK:")
print(CHUNK_ID)

print()
print("TESTO DEL CHUNK:")
print("-" * 80)
print(chunk_text)
print("-" * 80)


for index, query in enumerate(queries, start=1):

    query_embedding = create_embedding(query)

    distance = cosine_distance(
        query_embedding,
        chunk_embedding,
    )

    print()
    print("=" * 80)
    print(f"QUERY #{index}")
    print("=" * 80)

    print()
    print(query)

    print()
    print(f"Cosine distance: {distance:.4f}")


print()
print("=" * 80)
print("FINE TEST")
print("=" * 80)
