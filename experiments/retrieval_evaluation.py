
import chromadb


# -------------------------
# Vector database
# -------------------------

client = chromadb.Client()

collection = client.get_or_create_collection(
    name="evaluation"
)


# -------------------------
# Document chunks
# -------------------------

chunks = {
    "chunk-1": (
        "L'azienda è stata fondata nel 2018 "
        "e opera nel settore tecnologico."
    ),

    "chunk-2": (
        "Il contratto ha una durata di 24 mesi "
        "e può essere rinnovato alla scadenza."
    ),

    "chunk-3": (
        "Il canone mensile previsto dal contratto "
        "è di 1500 euro."
    ),

    "chunk-4": (
        "Il recesso deve essere comunicato con "
        "almeno 60 giorni di preavviso."
    ),

    "chunk-5": (
        "Il fatturato dell'azienda nell'ultimo "
        "esercizio è aumentato del 15%."
    )
}


# -------------------------
# Inserimento
# -------------------------

collection.add(
    documents=list(chunks.values()),
    ids=list(chunks.keys())
)


# -------------------------
# Dataset di evaluation
# -------------------------

tests = [
    {
        "question": "Quanto dura il contratto?",
        "expected_id": "chunk-2"
    },
    {
        "question": "Qual è il canone mensile?",
        "expected_id": "chunk-3"
    },
    {
        "question": "Come funziona il recesso?",
        "expected_id": "chunk-4"
    },
    {
        "question": "Quanto è aumentato il fatturato?",
        "expected_id": "chunk-5"
    }
]


# -------------------------
# Evaluation Top-3
# -------------------------

correct = 0

print()
print("RETRIEVAL EVALUATION - TOP 3")
print("============================")


for test in tests:

    results = collection.query(
        query_texts=[test["question"]],
        n_results=3
    )

    retrieved_ids = results["ids"][0]

    is_correct = (
        test["expected_id"] in retrieved_ids
    )

    if is_correct:
        correct += 1

    status = (
        "PASS"
        if is_correct
        else "FAIL"
    )

    print()
    print(f"[{status}]")
    print("Domanda:", test["question"])
    print("Atteso:", test["expected_id"])
    print("Trovati:", retrieved_ids)


# -------------------------
# Risultato finale
# -------------------------

total = len(tests)

accuracy = correct / total

print()
print("============================")
print(
    f"Top-3 Accuracy: {correct}/{total}"
)

print(
    f"Percentuale: {accuracy:.0%}"
)

