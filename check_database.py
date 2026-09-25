from app.db.database import SessionLocal
from app.db.models import Document


db = SessionLocal()

documents = db.query(Document).all()

for document in documents:
    print(
        document.id,
        "|",
        document.original_filename,
        "|",
        document.size_bytes,
        "bytes",
    )

db.close()