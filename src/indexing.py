from sentence_transformers import SentenceTransformer
import chromadb
from rank_bm25 import BM25Okapi

embedder = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
chroma_client = chromadb.Client()

def initialize_dense_index(name="enterprise_dense"):
    try:
        col = chroma_client.get_collection(name)
    except:
        col = chroma_client.create_collection(name)
    return col

def build_dense_index(collection, chunks):
    # clear to avoid duplicates
    try: chroma_client.delete_collection(collection.name)
    except: pass
    collection = chroma_client.create_collection(collection.name)

    docs = [c["content"] for c in chunks]
    ids  = [c["chunk_id"] for c in chunks]
    metas= [{"source":c["source"], "type":c["type"]} for c in chunks]

    embeds = embedder.encode(docs, convert_to_numpy=True)

    collection.add(
        embeddings=embeds.tolist(),
        ids=ids,
        documents=docs,
        metadatas=metas
    )

    return collection

def initialize_bm25(chunks):
    corpus = [c["content"].split() for c in chunks]
    return BM25Okapi(corpus)