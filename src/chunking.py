def chunk_text(text, source, size=600, overlap=100):
    if not text:
        return []
    chunks = []
    words = text.split()
    start = 0
    while start < len(words):
        chunk = " ".join(words[start:start+size])
        chunks.append(("text", chunk, source))
        start += size - overlap
    return chunks

def chunk_table(md_table, source, rows_per_chunk=8):
    if not md_table:
        return []
    rows = md_table.split("\n")
    if len(rows) < 3:
        return [("table", md_table, source)]
    header = rows[0:2]
    body = rows[2:]
    chunks = []
    for i in range(0, len(body), rows_per_chunk):
        chunk_rows = header + body[i:i+rows_per_chunk]
        chunks.append(("table", "\n".join(chunk_rows), source))
    return chunks

def chunk_image_text(ocr_text, source):
    if not ocr_text:
        return []
    return [("image", ocr_text, source)]
