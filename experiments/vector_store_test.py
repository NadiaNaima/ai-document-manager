import chromadb


# -------------------------
# Vector database
# -------------------------

client = chromadb.Client()


collection = client.get_or_create_collection(
    name="documents"
)


# -------------------------
# Document chunks
# -------------------------

chunks = [
    "L'azienda è stata fondata nel 2018 e opera nel settore tecnologico.",
    "Il contratto ha una durata di 24 mesi e può essere rinnovato alla scadenza.",
    "Il canone mensile previsto dal contratto è di 1500 euro.",
    "Il recesso deve essere comunicato con almeno 60 giorni di preavviso.",
    "Il fatturato dell'azienda nell'ultimo esercizio è aumentato del 15%."
]


# -------------------------
# Salvataggio
# -------------------------

collection.add(
    documents=chunks,
    ids=[
        "chunk-1",
        "chunk-2",
        "chunk-3",
        "chunk-4",
        "chunk-5"
    ]
)


print()
print("CHUNK SALVATI:")
print(collection.count())


# -------------------------
# Ricerca
# -------------------------

query = "Quanto dura il contratto?"

results = collection.query(
    query_texts=[query],
    n_results=3
)


print()
print("RICERCA:")
print(query)

print()
print("RISULTATI:")

for document in results["documents"][0]:
    print("-", document)