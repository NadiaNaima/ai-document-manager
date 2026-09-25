from app.services.vector_store import search_similar_chunks


DOCUMENT_ID = "test-real-pdf"
TOP_K = 3


tests = [
    {
        "question": "Quali documenti sono necessari per l'ingresso?",
        "relevant_chunks": [
            "test-real-pdf-chunk-1",
            "test-real-pdf-chunk-2",
        ],
    },
    {
        "question": "Quali sono i requisiti economici per l'ingresso?",
        "relevant_chunks": [
            "test-real-pdf-chunk-10",
        ],
    },
    {
        "question": "Attraverso quali luoghi è consentito entrare?",
        "relevant_chunks": [
            "test-real-pdf-chunk-2",
        ],
    },
    {
        "question": "È necessario fornire dati biometrici?",
        "relevant_chunks": [
            "test-real-pdf-chunk-14",
        ],
    },
]


evaluated_tests = []


print()
print("=" * 70)
print("RETRIEVAL EVALUATION - REAL PDF")
print("=" * 70)


for index, test in enumerate(tests, start=1):

    question = test["question"]
    relevant_chunks = test["relevant_chunks"]

    print()
    print(f"TEST {index}")
    print("-" * 70)
    print(f"Domanda: {question}")

    results = search_similar_chunks(
        document_id=DOCUMENT_ID,
        query=question,
        n_results=TOP_K,
    )

    ids = results["ids"][0]
    distances = results["distances"][0]

    print()
    print("Risultati:")

    for rank, chunk_id in enumerate(ids, start=1):

        distance = distances[rank - 1]

        print(
            f"{rank}. {chunk_id} "
            f"(distance={distance:.4f})"
        )

    top1_hit = ids[0] in relevant_chunks

    retrieved_top3 = ids[:TOP_K]

    top3_hits = [
        chunk_id
        for chunk_id in retrieved_top3
        if chunk_id in relevant_chunks
    ]

    top3_hit = len(top3_hits) > 0

    recall_at_3 = (
        len(top3_hits)
        / len(relevant_chunks)
    )

    print()
    print(
        "Top-1:",
        "PASS" if top1_hit else "FAIL"
    )

    print(
        "Top-3:",
        "PASS" if top3_hit else "FAIL"
    )

    print(
        f"Recall@3: "
        f"{recall_at_3:.2f} "
        f"({len(top3_hits)}/{len(relevant_chunks)})"
    )

    if top3_hits:
        print(
            "Chunk rilevanti recuperati:",
            ", ".join(top3_hits)
        )

    evaluated_tests.append(
        {
            "top1": top1_hit,
            "top3": top3_hit,
            "recall_at_3": recall_at_3,
        }
    )


print()
print("=" * 70)
print("RISULTATI FINALI")
print("=" * 70)


top1_accuracy = (
    sum(
        test["top1"]
        for test in evaluated_tests
    )
    / len(evaluated_tests)
)


top3_accuracy = (
    sum(
        test["top3"]
        for test in evaluated_tests
    )
    / len(evaluated_tests)
)


mean_recall_at_3 = (
    sum(
        test["recall_at_3"]
        for test in evaluated_tests
    )
    / len(evaluated_tests)
)


print()
print(
    f"Test valutati: "
    f"{len(evaluated_tests)}"
)


print(
    f"Top-1 Hit Rate: "
    f"{top1_accuracy:.1%}"
)


print(
    f"Top-3 Hit Rate: "
    f"{top3_accuracy:.1%}"
)


print(
    f"Mean Recall@3: "
    f"{mean_recall_at_3:.1%}"
)


print()
print("=" * 70)
print("FINE EVALUATION")
print("=" * 70)
