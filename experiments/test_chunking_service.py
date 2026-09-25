
from app.services.chunking_service import split_text


text = """
Questo è un documento di esempio.

Il contratto ha una durata di 24 mesi
e può essere rinnovato alla scadenza.

Il canone mensile previsto dal contratto
è di 1500 euro.

Il recesso deve essere comunicato con
almeno 60 giorni di preavviso.

Il fatturato dell'azienda nell'ultimo
esercizio è aumentato del 15%.
"""


chunks = split_text(
    text,
    chunk_size=100,
    overlap=20,
)


print()
print("NUMERO DI CHUNK:")
print(len(chunks))

print()

for index, chunk in enumerate(
    chunks,
    start=1,
):
    print(
        f"--- CHUNK {index} ---"
    )
    print(chunk)
    print()
