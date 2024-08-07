from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from common import LLM
from common.models import SaveTextRequest, TextEmbedding, GetTextResponse

from embedding_api.storage import Storage

app = FastAPI(title="Embedding API")
llm = LLM()
storage = Storage()


@app.post("/text")
def save_text(request: SaveTextRequest):
    vector = llm.embed(request.text)

    embedding_id = storage.save_embedding(
        TextEmbedding(text=request.text, source=request.source, vector=vector)
    )

    return {"id": embedding_id}


@app.get("/text", response_model=list[GetTextResponse])
def get_relevant_text(text: str, top_n: int = 1):
    vector = llm.embed(text)

    most_similar = storage.get_most_similar(
        TextEmbedding(text=text, source="query", vector=vector),
        top_n,
    )

    return [
        GetTextResponse(
            text=text.text,
            source=text.source,
            distance=text.distance,
        )
        for text in most_similar
    ]


@app.get("/")
def redirect_to_docs():
    return RedirectResponse(url="/docs")
