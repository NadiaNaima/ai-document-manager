
from pathlib import Path

from app.services.document_processor import extract_text_from_pdf
from app.services.chunking_service import split_text
from app.services.vector_store import add_chunk


PDF_PATH = Path("storage/test.pdf")
DOCUMENT_ID = "test-real-pdf"


if not PDF_PATH.exists():
    raise FileNotFoundError(
        f"PDF non trovato: {PDF_PATH}"
    )


print()
print("REAL PDF INDEXING")
print("=================")
print()

print("PDF:")
print(PDF_PATH)

# 1. Estrazione del testo
text = extract_text_from_pdf(str(PDF_PATH))

print()
print("TESTO ESTRATTO")
print("----------------")
print("Numero caratteri:", len(text))

# 2. Chunking
chunks = split_text(
    text,
    chunk_size=1000,
    overlap=200,
)

print()
print("CHUNKING")
print("----------------")
print("Numero chunk:", len(chunks))

# 3. Creazione embedding + salvataggio in ChromaDB
print()
print("INDICIZZAZIONE")
print("----------------")

for index, chunk in enumerate(chunks):
    chunk_id = f"{DOCUMENT_ID}-chunk-{index}"

    add_chunk(
        document_id=DOCUMENT_ID,
        chunk_id=chunk_id,
        text=chunk,
    )

    print(
        f"[OK] Chunk {index + 1}/{len(chunks)} "
        f"salvato"
    )

print()
print("Indicizzazione completata.")
