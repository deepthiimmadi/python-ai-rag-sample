"""Small RAG-style search over synthetic local documents.

No external LLM call is made by default. Retrieval is keyword-based so the
behaviour is explainable and testable without an API key.
"""

from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="python-ai-rag-sample")
DATA_DIR = Path(__file__).parent / "data"


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    sources: list[str]


def load_documents() -> list[tuple[str, str]]:
    """Return (filename, text) for every .md file in data/."""
    docs = []
    for path in sorted(DATA_DIR.glob("*.md")):
        docs.append((path.name, path.read_text(encoding="utf-8")))
    return docs


def score(question: str, text: str) -> int:
    """Simple keyword overlap score, ignoring very short words."""
    words = {w.strip(".,?") for w in question.lower().split() if len(w) > 3}
    text_lower = text.lower()
    return sum(1 for w in words if w in text_lower)


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    docs = load_documents()
    ranked = sorted(docs, key=lambda d: score(request.question, d[1]), reverse=True)
    top = [(name, text) for name, text in ranked if score(request.question, text) > 0][:2]

    if not top:
        return AskResponse(
            answer="I could not find anything relevant in the local documents.",
            sources=[],
        )

    summary = " ".join(text.splitlines()[0] for _, text in top)
    return AskResponse(
        answer=f"Based on the local documents: {summary}",
        sources=[name for name, _ in top],
    )
