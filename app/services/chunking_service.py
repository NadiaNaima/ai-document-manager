
def split_text(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 200,
) -> list[str]:
    """
    Divide il testo in chunk cercando di interrompere
    il testo in corrispondenza di un confine naturale.

    Il chunk può essere leggermente più corto o più lungo
    della dimensione richiesta per evitare di spezzare
    parole o frasi.
    """

    if not text:
        return []

    if chunk_size <= 0:
        raise ValueError("chunk_size deve essere maggiore di zero")

    if overlap < 0:
        raise ValueError("overlap non può essere negativo")

    if overlap >= chunk_size:
        raise ValueError("overlap deve essere inferiore a chunk_size")

    chunks = []

    start = 0
    step = chunk_size - overlap

    while start < len(text):
        target_end = start + chunk_size

        if target_end >= len(text):
            chunk = text[start:]
            if chunk.strip():
                chunks.append(chunk)
            break

        # Cerchiamo un punto naturale vicino alla fine desiderata.
        search_start = max(start, target_end - 100)

        boundary_positions = [
            text.rfind("\n\n", search_start, target_end),
            text.rfind(". ", search_start, target_end),
            text.rfind("? ", search_start, target_end),
            text.rfind("! ", search_start, target_end),
            text.rfind("\n", search_start, target_end),
            text.rfind(" ", search_start, target_end),
        ]

        boundary = max(boundary_positions)

        if boundary <= start:
            end = target_end
        else:
            # Per ". " e simili includiamo anche il carattere
            # di punteggiatura nel chunk.
            if text[boundary] in ".?!":
                end = boundary + 1
            else:
                end = boundary

        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk)

        # Manteniamo l'overlap.
        start = max(end - overlap, start + 1)

    return chunks
