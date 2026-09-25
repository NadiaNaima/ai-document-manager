from app.services.vector_store import search_similar_chunks


DOCUMENT_ID = "test-real-pdf"
TOP_K = 3


questions = [
    "Quali sono i requisiti economici per l'ingresso?",
    "Quanti soldi deve avere lo straniero per entrare?",
    "Quali mezzi di sussistenza sono richiesti?",
    "Quali sono le condizioni economiche per entrare in Italia?",
]


def test_question(index, question):

    print()
    print("=" * 80)
    print(f"DOMANDA #{index}")
    print("=" * 80)

    print()
    print(question)

    results = search_similar_chunks(
        document_id=DOCUMENT_ID,
        query=question,
        n_results=TOP_K,
    )

    ids = results["ids"][0]
    distances = results["distances"][0]

    print()
    print("RANKING")
    print("-" * 80)

    for rank, chunk_id in enumerate(ids, start=1):

        distance = distances[rank - 1]

        print(
            f"{rank}. {chunk_id} "
            f"-> distance = {distance:.4f}"
        )


print()
print("=" * 80)
print("SEMANTIC RANKING TEST")
print("=" * 80)


for index, question in enumerate(questions, start=1):
    test_question(index, question)


print()
print("=" * 80)
print("FINE TEST")
print("=" * 80)
