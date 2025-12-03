# RAY_AI_CASE_STUDY

## Enterprise Document Intelligence Demo with RAG

This repository demonstrates a **Retrieval-Augmented Generation (RAG)** pipeline for enterprise document analysis using free Hugging Face models. It ingests PDFs, tables, and images, extracts key information, and synthesizes structured outputs.

## Architecture Diagram

```mermaid
flowchart TD
    A["Documents Folder - PDFs, Tables, Images"] --> B["Ingestion Module (src/ingestion.py)"]
    B --> C["Chunking Module (src/chunking.py)"]
    C --> D["Hybrid Index - Dense + Sparse (src/hybrid_retrieval.py)"]
    D --> E["Agent (src/agent.py) with LLM"]
    E --> F["Structured JSON Output & Summaries"]
```

## Evaluation Example
I utilized the Case study shared to me by RAY AI to evaluate the performance of my model and the output with regards to the predetermined queries which are:
1. Summarize key product specifications.
2. List numerical data in the report.
3. Identify risks highlighted in the documents.
4. Provide overall insights.
---
