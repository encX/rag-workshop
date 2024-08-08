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

    response_json = requests.get(
        f"http://{config.embedding_api_host}/text?text={last_message}&top_n=3"
    ).json()
    embeddings = [GetTextResponse(**item) for item in response_json]

    system_message = __get_system_message(embeddings)

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


def __get_system_message(embeddings: List[GetTextResponse]) -> str:
    knowledge = "\n".join([embedding.text for embedding in embeddings])

    return f"""
You are an AI assistant designed to provide information solely based on the internal knowledge contained in the context. Your responses should be:

1. Strictly limited to the information available in the embeddings
2. Clear and concise
3. Factual and objective

If asked about topics not covered in the context:
- Politely state that you don't have information on that topic
- Avoid speculating or providing information from outside sources

Your primary goal is to accurately relay internal information to users. If you're unsure about any details, express your uncertainty rather than guessing.

Remember:
- Do not use external knowledge or current events in your responses
- Always base your answers on the provided context
- If clarification is needed, ask the user for more details

Respond to queries to the best of your ability using only the knowledge contained in the context.

Context:
{knowledge}"""