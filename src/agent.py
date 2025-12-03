from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from .hybrid_retrieval import hybrid_retrieve

model_id = "microsoft/phi-1_5"   
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto")
llm = pipeline("text-generation", model=model, tokenizer=tokenizer)

rag_prompt = """
You are an enterprise document intelligence agent.

Given the retrieved evidence chunks below, you must:

1. Use ONLY the retrieved chunks.
2. Cite chunks using their metadata.
3. Explain WHY each chunk was retrieved (keyword match or semantic relevance).
4. Provide a final answer.
5. Provide JSON output:

{
  "key_findings": [],
  "numerical_data": [],
  "risk_flags": [],
  "insights": []
}

Retrieved Evidence:
{evidence}

Question:
{query}

If evidence is insufficient, answer: "INSUFFICIENT EVIDENCE".
"""

def run_agent(query, chunks, dense_db, bm25, k=5):
    retrieved = hybrid_retrieve(query, chunks, dense_db, bm25, k)

    ev = ""
    for r in retrieved:
        ev += f"[{r['chunk_id']} | {r['source']} | score={r['fused_score']:.4f}]\n{r['content']}\n\n"

    prompt = rag_prompt.format(evidence=ev, query=query)
    output = llm(prompt, max_length=1200, do_sample=False)[0]["generated_text"]
    return output