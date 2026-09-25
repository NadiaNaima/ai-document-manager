from app.services.embedding_service import create_embedding


text = "Il contratto ha una durata di 24 mesi."


embedding = create_embedding(text)


print()
print("Embedding creato")
print("-------------------------")
print("Numero valori:", len(embedding))
print("Primi 10 valori:", embedding[:10])