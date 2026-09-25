import os
import math

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY non configurata"
    )

client = genai.Client(
    api_key=api_key
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
# Embedding
# -------------------------

def create_embedding(text):

    result = client.models.embed_content(
        model="gemini-embedding-2",
        contents=text,
        config=types.EmbedContentConfig(
            output_dimensionality=768
        )
    )

    return result.embeddings[0].values


# -------------------------
# Cosine similarity
# -------------------------

def cosine_similarity(vector_a, vector_b):

    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    return dot_product / (
        magnitude_a * magnitude_b
    )


# -------------------------
# Query
# -------------------------

query = "Quanto dura il contratto?"

print()
print("DOMANDA:")
print(query)


query_embedding = create_embedding(query)


# -------------------------
# Search
# -------------------------

results = []

for chunk in chunks:

    chunk_embedding = create_embedding(chunk)

    similarity = cosine_similarity(
        query_embedding,
        chunk_embedding
    )

    results.append(
        {
            "chunk": chunk,
            "similarity": similarity
        }
    )


# -------------------------
# Ordinamento
# -------------------------

results.sort(
    key=lambda item: item["similarity"],
    reverse=True
)


# -------------------------
# Risultati
# -------------------------

print()
print("RISULTATI")
print("-------------------------")

for result in results:

    print(
        f"{result['similarity']:.4f}"
        f" → "
        f"{result['chunk']}"
    )