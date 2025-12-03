from sentence_transformers import SentenceTransformer
import chromadb
from rank_bm25 import BM25Okapi

embedder = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
chroma_client = chromadb.Client()

def initialize_dense_index(collection_name="enterprise_dense"):
    try:
        collection = chroma_client.get_collection(collection_name)
    except Exception:
        collection = chroma_client.create_collection(collection_name)
    return collection, embedder


def initialize_bm25(chunks):
    corpus = [c[1].split() for c in chunks] 
    return BM25Okapi(corpus)

def fuse_scores_rrf(dense_results, sparse_scores, k=10):

    combined = []
    for i, s_score in enumerate(sparse_scores):
        d_score = dense_results[i]['score'] if i < len(dense_results) else 0
        combined.append({'index': i, 'rrf': 1/(60+1/(d_score+1e-6)) + 1/(60+1/(s_score+1e-6))})
    return combined

def hybrid_retrieve(query, chunks, dense_db, bm25, k=5):
    # Dense
    q_emb = embedder.encode([query])[0]
    dense_results = dense_db.query(query_embeddings=[q_emb], n_results=min(10, len(chunks)))

    # Sparse
    sparse_scores = bm25.get_scores(query.split())

    # Fuse
    combined = fuse_scores_rrf(dense_results, sparse_scores)

    # Sort by RRF
    top_indices = sorted(range(len(combined)), key=lambda i: combined[i]['rrf'], reverse=True)[:k]

    # Return chunks with metadata
    return [ 
        {
            "type": chunks[i][0],
            "content": chunks[i][1],
            "source": chunks[i][2],
            "score": combined[i]['rrf']
        } 
        for i in top_indices
    ]

def load_or_build_indexes(chunks, rebuild=False):
    dense_db, embedder_model = initialize_dense_index()
    bm25_index = initialize_bm25(chunks)
    return {"dense": dense_db, "embedder": embedder_model, "bm25": bm25_index, "chunks": chunks}