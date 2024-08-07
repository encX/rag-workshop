from typing import List
from openai import OpenAI

from common.config import config
from common.models import ChatCompletionMessage


class LLM:
    __embedding_model = "text-embedding-3-small"
    __chat_completion_model = "gpt-4o-mini"

    def __init__(self):
        self.__openai = OpenAI(api_key=config.openai.api_key, base_url=config.openai.base_url)

    def embed(self, text: str) -> List[float]:
        return (
            self.__openai.embeddings.create(input=[text], model=self.__embedding_model)
            .data[0]
            .embedding
        )

    def complete_chat(self, conversation: List[ChatCompletionMessage]) -> str:
        response = self.__openai.chat.completions.create(
            model=self.__chat_completion_model,
            messages=conversation,
        )

        return response.choices[0].message.content
