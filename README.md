# python-ai-rag-sample

A small, sanitised Python sample showing a RAG-style search over local documents:
load synthetic documents, retrieve the most relevant ones by keyword, and
return a grounded answer that cites the documents it used.

This is a learning sample only. It contains no client data, no real documents,
and no production LLM call by default. All documents in `data/` are synthetic.

## What it shows

- FastAPI service with a single `/ask` endpoint
- Simple, explainable retrieval: chunking + keyword scoring
- Grounded answers: every answer lists the source documents it used
- A clear place to plug in a real embedding model / vector store and an LLM,
  without changing the API

## Run it

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Then ask, for example:

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "How do I submit a case for approval?"}'
```

## How to make it production-grade

- Replace keyword retrieval with embeddings and a vector store
- Add an LLM call with a prompt that only uses the retrieved context
- Add guardrails: no personal data in prompts, logging, cost limits, and
  a fallback answer when nothing relevant is retrieved
- Add tests for retrieval: a question should return the document it was written from
