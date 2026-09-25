from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db.models import Document
from app.services.ai_service import ask_document, generate_summary
from app.services.document_processor import extract_text_from_pdf


router = APIRouter()


class AskDocumentRequest(BaseModel):
    question: str


STORAGE_DIR = Path("storage")
STORAGE_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".xlsx",
    ".txt",
}


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing",
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type {extension} is not allowed",
        )

    document_id = str(uuid4())
    stored_filename = f"{document_id}{extension}"
    file_path = STORAGE_DIR / stored_filename

    content = await file.read()

    file_path.write_bytes(content)

    extracted_text = None
    ai_summary = None

    if extension == ".pdf":
        extracted_text = extract_text_from_pdf(
            str(file_path)
        )

        if extracted_text:
            ai_summary = generate_summary(
                extracted_text
            )

    db: Session = SessionLocal()

    try:
        document = Document(
            id=document_id,
            original_filename=file.filename,
            stored_filename=stored_filename,
            content_type=file.content_type,
            size_bytes=len(content),
            file_path=str(file_path),
            extracted_text=extracted_text,
            ai_summary=ai_summary,
        )

        db.add(document)

        db.commit()

        db.refresh(document)

    except Exception:
        db.rollback()

        if file_path.exists():
            file_path.unlink()

        raise

    finally:
        db.close()

    return {
        "document_id": document.id,
        "original_filename": document.original_filename,
        "stored_filename": document.stored_filename,
        "content_type": document.content_type,
        "size_bytes": document.size_bytes,
        "file_path": document.file_path,
        "extracted_text_length": len(extracted_text or ""),
        "ai_summary": ai_summary,
        "message": "Document uploaded successfully",
    }


@router.get("/")
def get_documents():
    db: Session = SessionLocal()

    try:
        documents = db.query(Document).all()

        return [
            {
                "document_id": document.id,
                "original_filename": document.original_filename,
                "content_type": document.content_type,
                "size_bytes": document.size_bytes,
                "file_path": document.file_path,
                "created_at": document.created_at,
            }
            for document in documents
        ]

    finally:
        db.close()


@router.get("/{document_id}/text")
def get_document_text(document_id: str):
    db: Session = SessionLocal()

    try:
        document = (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

        if document is None:
            raise HTTPException(
                status_code=404,
                detail="Document not found",
            )

        return {
            "document_id": document.id,
            "filename": document.original_filename,
            "text": document.extracted_text or "",
            "text_length": len(document.extracted_text or ""),
        }

    finally:
        db.close()


@router.get("/{document_id}/summary")
def get_document_summary(document_id: str):
    db: Session = SessionLocal()

    try:
        document = (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

        if document is None:
            raise HTTPException(
                status_code=404,
                detail="Document not found",
            )

        return {
            "document_id": document.id,
            "filename": document.original_filename,
            "summary": document.ai_summary or "",
        }

    finally:
        db.close()


@router.post("/{document_id}/ask")
def ask_document_question(
    document_id: str,
    request: AskDocumentRequest,
):
    db: Session = SessionLocal()

    try:
        document = (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

        if document is None:
            raise HTTPException(
                status_code=404,
                detail="Document not found",
            )

        if not document.extracted_text:
            raise HTTPException(
                status_code=400,
                detail="Document has no extracted text",
            )

        if not request.question.strip():
            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty",
            )

        answer = ask_document(
            document.extracted_text,
            request.question,
        )

        return {
            "document_id": document.id,
            "filename": document.original_filename,
            "question": request.question,
            "answer": answer,
        }

    finally:
        db.close()

@router.get("/{document_id}/download")
def download_document(document_id: str):
    db: Session = SessionLocal()

    try:
        document = (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

        if document is None:
            raise HTTPException(
                status_code=404,
                detail="Document not found",
            )

        file_path = Path(document.file_path)

        if not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail="File not found",
            )

        return FileResponse(
            path=file_path,
            filename=document.original_filename,
            media_type=document.content_type,
        )

    finally:
        db.close()
@router.get("/{document_id}")
def get_document(document_id: str):
    db: Session = SessionLocal()

    try:
        document = (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

        if document is None:
            raise HTTPException(
                status_code=404,
                detail="Document not found",
            )

        return {
            "document_id": document.id,
            "original_filename": document.original_filename,
            "stored_filename": document.stored_filename,
            "content_type": document.content_type,
            "size_bytes": document.size_bytes,
            "file_path": document.file_path,
            "extracted_text": document.extracted_text or "",
            "ai_summary": document.ai_summary or "",
            "created_at": document.created_at,
        }

    finally:
        db.close()


@router.delete("/{document_id}")
def delete_document(document_id: str):
    db: Session = SessionLocal()

    try:
        document = (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

        if document is None:
            raise HTTPException(
                status_code=404,
                detail="Document not found",
            )

        file_path = Path(document.file_path)

        db.delete(document)

        db.commit()

        if file_path.exists():
            file_path.unlink()

        return {
            "document_id": document_id,
            "message": "Document deleted successfully",
        }

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()