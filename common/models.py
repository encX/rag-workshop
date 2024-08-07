from typing import List

from pydantic import BaseModel


class ChatRequest(BaseModel):
    messages: list[str]


class ChatCompletionMessage(BaseModel):
    role: str
    content: str


class TextEmbedding(BaseModel):
    text: str
    source: str
    vector: List[float]
    distance: float = None


class SaveTextRequest(BaseModel):
    text: str
    source: str


class GetTextResponse(BaseModel):
    text: str
    source: str
    distance: float
