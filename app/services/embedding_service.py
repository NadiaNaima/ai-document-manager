
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


# -------------------------
# Configurazione
# -------------------------

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
# Creazione embedding
# -------------------------

def create_embedding(text: str) -> list[float]:
    """
    Trasforma un testo in un embedding numerico.
    """

    result = client.models.embed_content(
        model="gemini-embedding-2",
        contents=text,
        config=types.EmbedContentConfig(
            output_dimensionality=768
        )
    )

    return result.embeddings[0].values

