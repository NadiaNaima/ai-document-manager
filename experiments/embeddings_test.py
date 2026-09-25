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


texts = [
    "Il contratto ha una durata di 24 mesi.",
    "L'accordo è valido per due anni.",
    "Il fatturato dell'azienda è aumentato del 15%."
]


embeddings = []


for text in texts:

    result = client.models.embed_content(
        model="gemini-embedding-2",
        contents=text,
        config=types.EmbedContentConfig(
            output_dimensionality=768
        )
    )

    embedding = result.embeddings[0].values

    embeddings.append(embedding)


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


similarity_ab = cosine_similarity(
    embeddings[0],
    embeddings[1]
)

similarity_ac = cosine_similarity(
    embeddings[0],
    embeddings[2]
)

similarity_bc = cosine_similarity(
    embeddings[1],
    embeddings[2]
)


print()
print("SIMILARITÀ")
print("-------------------------")

print(
    "Contratto ↔ Accordo:",
    similarity_ab
)

print(
    "Contratto ↔ Fatturato:",
    similarity_ac
)

print(
    "Accordo ↔ Fatturato:",
    similarity_bc
)