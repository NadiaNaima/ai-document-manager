from app.services.document_processor import extract_text_from_pdf


file_path = "storage/test.pdf"

text = extract_text_from_pdf(file_path)

print("Extracted text:")
print("=" * 50)
print(text[:3000])