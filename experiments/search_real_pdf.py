
from app.services.vector_store import search_similar_chunks


DOCUMENT_ID = "test-real-pdf"


question = input(
    "Inserisci una domanda sul documento: "
)

results = search_similar_chunks(
    document_id=DOCUMENT_ID,
    query=question,
    n_results=3,
)

print()
print("SEMANTIC SEARCH")
print("================")
print()

print("DOMANDA:")
print(question)

print()
print("CHUNK RECUPERATI")
print("----------------")

documents = results["documents"][0]
distances = results["distances"][0]
ids = results["ids"][0]

for index, (chunk_id, document, distance) in enumerate(
    zip(ids, documents, distances),
    start=1,
):
    print()
    print(f"--- RISULTATO {index} ---")
    print("ID:", chunk_id)
    print("Distanza:", distance)
    print()
    print(document)

