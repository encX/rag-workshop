import requests

from typing import List
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from common import config, LLM
from common.models import ChatRequest, GetTextResponse, ChatCompletionMessage

app = FastAPI(title="Chatbot")
llm = LLM()

app.mount("/static", StaticFiles(directory="chatbot/static"), name="static")
templates = Jinja2Templates(directory="chatbot/templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(name="index.html", request=request)


@app.post("/chat", response_class=JSONResponse)
def chat(request: ChatRequest):
    conversation = request.messages
    last_message = conversation[-1]

    system_message = __get_system_message()

    chat_completion_messages = __build_conversation(conversation, system_message)

    ai_response = llm.complete_chat(chat_completion_messages)

    return {"response": ai_response}


def __build_conversation(
    conversation: List[str], system_message: str
) -> List[ChatCompletionMessage]:
    system = [ChatCompletionMessage(role="system", content=system_message)]
    chat = [
        ChatCompletionMessage(
            role="user" if i % 2 == 0 else "assistant", content=message
        )
        for i, message in enumerate(conversation)
    ]

    return system + chat


def __get_system_message() -> str:
    return "You are a helpful assistant."