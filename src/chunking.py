def chunk_text(text, source, size=600, overlap=100):
    if not text: return []
    chunks, words, i = [], text.split(), 0
    cid = 0
    while i < len(words):
        chunk = " ".join(words[i:i+size])
        chunks.append({
            "chunk_id": f"{source}_text_{cid}",
            "content": chunk,
            "type": "text",
            "source": source
        })
        i += size - overlap
        cid += 1
    return chunks

def chunk_table(md_table, source, rows_per_chunk=8):
    if not md_table: return []
    rows = md_table.split("\n")
    header, body = rows[:2], rows[2:]
    chunks = []
    for i in range(0, len(body), rows_per_chunk):
        part = header + body[i:i+rows_per_chunk]
        chunks.append({
            "chunk_id": f"{source}_table_{i}",
            "content": "\n".join(part),
            "type": "table",
            "source": source
        })
    return chunks

def chunk_image_text(text, source):
    if not text: return []
    return [{
        "chunk_id": f"{source}_img_0",
        "content": text,
        "type": "image",
        "source": source
    }]