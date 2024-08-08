import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from common import config
from common.models import GetTextResponse

app = FastAPI(title="Search Web")

app.mount("/static", StaticFiles(directory="search_web/static"), name="static")
templates = Jinja2Templates(directory="search_web/templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(name="index.html", request=request)


@app.get("/search", response_class=HTMLResponse)
def search(request: Request, term: str):
    if not term:
        return RedirectResponse(url="/")

    # send search_term to get embeddings from embedding_api
    embeddings = []

    return templates.TemplateResponse(
        name="search_result.html",
        request=request,
        context={"term": term, "embeddings": embeddings},
    )
