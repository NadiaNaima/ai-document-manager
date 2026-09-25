import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


api_key = os.getenv("GEMINI_API_KEY")
ai_enabled = os.getenv("AI_ENABLED", "true").lower() == "true"


if ai_enabled and not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured"
    )


client = (
    genai.Client(
        api_key=api_key,
        http_options={
            "api_version": "v1"
        }
    )
    if ai_enabled
    else None
)


def generate_summary(text: str) -> str:
    if not ai_enabled:
        return "AI disabled"

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=(
            "You are a document analysis assistant. "
            "Summarize the provided business document "
            "clearly and accurately. "
            "Do not invent information.\n\n"
            "Document:\n"
            f"{text}"
        ),
    )

    return interaction.output_text


def ask_document(text: str, question: str) -> str:
    if not ai_enabled:
        return "AI disabled"

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=(
            "You are a document analysis assistant. "
            "Answer the user's question using only the "
            "information contained in the document. "
            "If the answer is not present in the document, "
            "say that the information is not available. "
            "Do not invent information.\n\n"
            "Document:\n"
            f"{text}\n\n"
            "Question:\n"
            f"{question}"
        ),
    )

    return interaction.output_text