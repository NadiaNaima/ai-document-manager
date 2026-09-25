
from app.services.vector_store import search_similar_chunks
from app.services.ai_service import client, ai_enabled


DOCUMENT_ID = "test-real-pdf"


tests = [
    "Quali documenti sono necessari per l'ingresso?",
    "Quali sono i requisiti economici per l'ingresso?",
    "Attraverso quali luoghi è consentito entrare?",
    "È necessario fornire dati biometrici?",
    "Qual è la durata del soggiorno?",
]


def generate_answer(question: str, context: str) -> str:
    """
    Genera una risposta usando esclusivamente
    il contesto recuperato dal vector store.
    """

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=(
            "Sei un assistente che analizza documenti. "
            "Rispondi alla domanda usando esclusivamente "
            "le informazioni presenti nel contesto. "
            "Se il contesto non contiene informazioni "
            "sufficienti per rispondere, "
            "dichiara che l'informazione non è disponibile "
            "nel contesto. "
            "Non usare conoscenze esterne e non inventare "
            "informazioni.\n\n"
            "CONTESTO:\n"
            f"{context}\n\n"
            "DOMANDA:\n"
            f"{question}"
        ),
    )

    return interaction.output_text


if not ai_enabled:
    raise RuntimeError(
        "AI_ENABLED deve essere true per eseguire questo test."
    )


for index, question in enumerate(tests, start=1):

    # ==================================================
    # 1. RETRIEVAL
    # ==================================================

    results = search_similar_chunks(
        document_id=DOCUMENT_ID,
        query=question,
        n_results=3,
    )

    documents = results["documents"][0]
    ids = results["ids"][0]
    distances = results["distances"][0]

    context = "\n\n".join(
        f"- {document}"
        for document in documents
    )

    print()
    print("=" * 70)
    print(f"TEST {index}")
    print("=" * 70)

    print()
    print("DOMANDA:")
    print(question)

    print()
    print("CHUNK RECUPERATI")
    print("-----------------")

    for chunk_index, (
        chunk_id,
        document,
        distance,
    ) in enumerate(
        zip(ids, documents, distances),
        start=1,
    ):
        print()
        print(f"--- CHUNK {chunk_index} ---")
        print("ID:", chunk_id)
        print("Distanza:", distance)
        print()
        print(document[:500])

    # ==================================================
    # 2. GENERATION
    # ==================================================

    try:
        answer = generate_answer(
            question,
            context,
        )

        print()
        print("RISPOSTA")
        print("--------")
        print(answer)

    except Exception as error:
        print()
        print("ERRORE GENERAZIONE")
        print("------------------")
        print(error)

        print()
        print(
            "Il retrieval è stato completato, "
            "ma la generazione non è riuscita."
        )

        print(
            "Il test continua con la domanda successiva."
        )

