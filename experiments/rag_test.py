import os

import chromadb
from dotenv import load_dotenv
from google import genai


# -------------------------
# Configurazione Gemini
# -------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY non configurata"
    )

gemini_client = genai.Client(
    api_key=api_key
)


# -------------------------
# Vector database
# -------------------------

chroma_client = chromadb.Client()

collection = chroma_client.get_or_create_collection(
    name="rag_test"
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
# Salvataggio chunks
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


# -------------------------
# Domanda
# -------------------------

question = "Quanto dura il contratto?"


# -------------------------
# Retrieval
# -------------------------

results = collection.query(
    query_texts=[question],
    n_results=3
)


retrieved_chunks = results["documents"][0]


print()
print("DOMANDA:")
print(question)

print()
print("CONTESTO RECUPERATO:")
print("-------------------------")

for chunk in retrieved_chunks:
    print("-", chunk)


# -------------------------
# Prompt RAG
# -------------------------

context = "\n".join(
    retrieved_chunks
)


prompt = f"""
Sei un assistente per l'analisi di documenti.

Rispondi alla domanda utilizzando
esclusivamente le informazioni presenti
nel CONTENUTO fornito.

Se la risposta non è presente nel contenuto,
rispondi che l'informazione non è disponibile.

Non inventare informazioni.

CONTENUTO:
{context}

DOMANDA:
{question}
"""


# -------------------------
# Generation
# -------------------------

response = gemini_client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)


print()
print("RISPOSTA:")
print("-------------------------")
print(response.text)