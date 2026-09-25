def split_text(text, chunk_size=100, overlap=20):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


text = """
Questo è un documento di esempio.
Il contratto ha una durata di 24 mesi.
Il canone mensile è di 1500 euro.
Il recesso deve essere comunicato con 60 giorni di preavviso.
Il contratto può essere rinnovato alla scadenza.
"""

chunks = split_text(text, chunk_size=100)

for index, chunk in enumerate(chunks, start=1):
    print(f"\n--- CHUNK {index} ---")
    print(chunk)