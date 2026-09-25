from app.services.vector_store import (
    add_chunk,
    search_similar_chunks,
)


document_id = "test-document"


chunks = [
    (
        "chunk-1",
        "L'azienda è stata fondata nel 2018 "
        "e opera nel settore tecnologico."
    ),
    (
        "chunk-2",
        "Il contratto ha una durata di 24 mesi "
        "e può essere rinnovato alla scadenza."
    ),
    (
        "chunk-3",
        "Il canone mensile previsto dal contratto "
        "è di 1500 euro."
    ),
    (
        "chunk-4",
        "Il recesso deve essere comunicato con "
        "almeno 60 giorni di preavviso."
    ),
    (
        "chunk-5",
        "Il fatturato dell'azienda nell'ultimo "
        "esercizio è aumentato del 15%."
    ),
]


# -------------------------
# Inserimento
# -------------------------

for chunk_id, text in chunks:

    add_chunk(
        document_id=document_id,
        chunk_id=chunk_id,
        text=text,
    )


print()
print("Chunk salvati.")


# -------------------------
# Ricerca
# -------------------------

query = "Quanto dura il contratto?"

results = search_similar_chunks(
    document_id=document_id,
    query=query,
    n_results=3,
)


print()
print("DOMANDA:")
print(query)

print()
print("RISULTATI:")
print("-------------------------")

for document in results["documents"][0]:
    print("-", document)