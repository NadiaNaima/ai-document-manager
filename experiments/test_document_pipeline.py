
from pathlib import Path

from app.services.document_processor import extract_text_from_pdf
from app.services.chunking_service import split_text


# -------------------------
# PDF di test
# -------------------------

pdf_path = Path(
    "storage/test.pdf"
)


# -------------------------
# Verifica file
# -------------------------

if not pdf_path.exists():
    raise FileNotFoundError(
        f"PDF non trovato: {pdf_path}"
    )


print()
print("DOCUMENT PIPELINE TEST")
print("======================")
print()

print("PDF:")
print(pdf_path)


# -------------------------
# Estrazione testo
# -------------------------

text = extract_text_from_pdf(
    str(pdf_path)
)


print()
print("TESTO ESTRATTO")
print("----------------------")

print(
    "Numero caratteri:",
    len(text)
)


# -------------------------
# Chunking
# -------------------------

chunks = split_text(
    text,
    chunk_size=1000,
    overlap=200,
)


print()
print("CHUNKING")
print("----------------------")

print(
    "Numero chunk:",
    len(chunks)
)


# -------------------------
# Mostra primi chunk
# -------------------------

for index, chunk in enumerate(
    chunks[:5],
    start=1,
):

    print()
    print(
        f"--- CHUNK {index} ---"
    )

    print(chunk[:500])

    print()
