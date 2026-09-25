from app.services.vector_store import search_similar_chunks

DOCUMENT_ID = "test-real-pdf"

question = "Quali sono i requisiti economici per l'ingresso?"

results = search_similar_chunks(
document_id=DOCUMENT_ID,
query=question,
n_results=3,
)

print()
print("=" * 80)
print("DEBUG CHROMA RESULTS")
print("=" * 80)

print()
print("TYPE RESULTS:")
print(type(results))

print()
print("RESULT KEYS:")
print(results.keys())

print()
print("IDS:")
print(results["ids"])

print()
print("DOCUMENTS:")
print(results["documents"])

print()
print("DISTANCES:")
print(results["distances"])

print()
print("=" * 80)
print("LENGTHS")
print("=" * 80)

print()
print("IDs:")
print(len(results["ids"][0]))

print()
print("Documents:")
print(len(results["documents"][0]))

print()
print("Distances:")
print(len(results["distances"][0]))

print()
print("=" * 80)
print("FINE DEBUG")
print("=" * 80)
