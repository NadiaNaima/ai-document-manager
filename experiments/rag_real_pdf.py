
from app.services.vector_store import search_similar_chunks
from app.services.ai_service import client, ai_enabled


DOCUMENT_ID = "test-real-pdf"


question = input(
    "Inserisci una domanda sul documento: "
)

# 1. Retrieval
results = search_similar_chunks(
    document_id=DOCUMENT_ID,
    query=question,
    n_results=3,
)

documents = results["documents"][0]

# 2. Costruiamo il contesto
context = "\n\n".join(
    f"- {document}"
    for document in documents
)

print()
print("RAG TEST")
print("========")
print()

print("DOMANDA:")
print(question)

print()
print("CONTESTO RECUPERATO")
print("-------------------")
print(context)

# 3. Generation
if not ai_enabled:
    print()
    print("AI disabilitata.")
else:
    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=(
            "Sei un assistente che analizza documenti. "
            "Rispondi alla domanda usando esclusivamente "
            "le informazioni presenti nel contesto fornito. "
            "Se il contesto non contiene informazioni "
            "sufficienti per rispondere, dichiaralo "
            "esplicitamente. "
            "Non inventare informazioni.\n\n"
            "CONTESTO:\n"
            f"{context}\n\n"
            "DOMANDA:\n"
            f"{question}"
        ),
    )

    print()
    print("RISPOSTA")
    print("--------")
    print(interaction.output_text)

