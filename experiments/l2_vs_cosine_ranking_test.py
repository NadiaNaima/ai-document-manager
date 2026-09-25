from app.services.embedding_service import create_embedding
from app.services.vector_store import collection


DOCUMENT_ID = "test-real-pdf"

QUERY = "Quali mezzi di sussistenza sono richiesti?"

TOP_K = 10


def cosine_similarity(vector_a, vector_b):
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

    return dot_product / (norm_a * norm_b)


def cosine_distance(vector_a, vector_b):
    return 1 - cosine_similarity(vector_a, vector_b)


def squared_l2_distance(vector_a, vector_b):
    return sum(
        (a - b) ** 2
        for a, b in zip(vector_a, vector_b)
    )


print()
print("=" * 80)
print("L2 VS COSINE RANKING TEST")
print("=" * 80)

print()
print("QUERY:")
print(QUERY)

query_embedding = create_embedding(QUERY)

result = collection.get(
    where={"document_id": DOCUMENT_ID},
    include=["documents", "embeddings"],
)

documents = result["documents"]
embeddings = result["embeddings"]

rows = []

for index, embedding in enumerate(embeddings):
    chunk_id = f"{DOCUMENT_ID}-chunk-{index}"

    cosine_dist = cosine_distance(
        query_embedding,
        embedding,
    )

    l2_dist = squared_l2_distance(
        query_embedding,
        embedding,
    )

    rows.append(
        {
            "chunk_id": chunk_id,
            "cosine_distance": cosine_dist,
            "l2_squared": l2_dist,
        }
    )


cosine_ranking = sorted(
    rows,
    key=lambda row: row["cosine_distance"],
)

l2_ranking = sorted(
    rows,
    key=lambda row: row["l2_squared"],
)


print()
print("=" * 80)
print("RANKING CON COSINE DISTANCE")
print("=" * 80)

for rank, row in enumerate(
    cosine_ranking[:TOP_K],
    start=1,
):
    print(
        f"{rank:2}. {row['chunk_id']} "
        f"-> cosine distance = "
        f"{row['cosine_distance']:.6f}"
    )


print()
print("=" * 80)
print("RANKING CON L2 SQUARED")
print("=" * 80)

for rank, row in enumerate(
    l2_ranking[:TOP_K],
    start=1,
):
    print(
        f"{rank:2}. {row['chunk_id']} "
        f"-> L2 squared = "
        f"{row['l2_squared']:.6f}"
    )


print()
print("=" * 80)
print("CONFRONTO TOP 10")
print("=" * 80)

for position in range(TOP_K):
    cosine_chunk = cosine_ranking[position]["chunk_id"]
    l2_chunk = l2_ranking[position]["chunk_id"]

    same = cosine_chunk == l2_chunk

    print(
        f"Posizione {position + 1:2}: "
        f"cosine={cosine_chunk} | "
        f"l2={l2_chunk} | "
        f"stesso={same}"
    )


print()
print("=" * 80)
print("FINE TEST")
print("=" * 80)
