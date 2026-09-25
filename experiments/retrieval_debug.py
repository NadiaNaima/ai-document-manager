from app.services.vector_store import search_similar_chunks

DOCUMENT_ID = "test-real-pdf"
TOP_K = 3

question = "Quali mezzi di sussistenza sono richiesti?"

results = search_similar_chunks(
document_id=DOCUMENT_ID,
query=question,
n_results=TOP_K,
)

ids = results["ids"][0]
documents = results["documents"][0]
distances = results["distances"][0]

print()
print("=" * 80)
print("RETRIEVAL DEBUG")
print("=" * 80)

print()
print("DOMANDA:")
print(question)

for rank in range(len(ids)):

    print()
    print("=" * 80)
    print(f"RANK #{rank + 1}")
    print("=" * 80)

    print()
    print("CHUNK ID:")
    print(ids[rank])

    print()
    print("DISTANCE:")
    print(f"{distances[rank]:.4f}")

    print()
    print("TESTO:")
    print("-" * 80)
    print(documents[rank])
    print("-" * 80)


print()
print("=" * 80)
print("FINE DEBUG")
print("=" * 80)
