from sentence_transformers import SentenceTransformer
import chromadb
from rank_bm25 import BM25Okapi

def hybrid_retrieve(query, chunks, dense_db, bm25, k=5):
    q_emb = embedder.encode([query])[0]
    dense_res = dense_db.query(query_embeddings=[q_emb], n_results=len(chunks))

    dense_ids = dense_res["ids"][0]
    dense_dist= dense_res["distances"][0]
    dmap = {cid:dist for cid,dist in zip(dense_ids, dense_dist)}

    sparse_scores = bm25.get_scores(query.split())

    results = []
    for i, ch in enumerate(chunks):
        cid = ch["chunk_id"]

        # distance → similarity
        dsim = 1 / (1 + dmap.get(cid, 999))

        bm = sparse_scores[i]
        bsim = bm / (1 + bm) if bm > 0 else 0

        results.append({
            "chunk_id": cid,
            "content": ch["content"],
            "source": ch["source"],
            "type": ch["type"],
            "fused_score": dsim + bsim
        })

    return sorted(results, key=lambda x: x["fused_score"], reverse=True)[:k]