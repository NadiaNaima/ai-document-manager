from pathlib import Path

import fitz


def extract_text_from_pdf(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    text_parts = []

    with fitz.open(path) as pdf:
        for page in pdf:
            text = page.get_text()

            if text:
                text_parts.append(text)

    return "\n".join(text_parts).strip()