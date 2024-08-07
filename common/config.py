import os

from dotenv import load_dotenv

load_dotenv()


class OpenAIConfig:
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")


class DatabaseConfig:
    connection_string = os.getenv("POSTGRES_CONNECTION_STRING")


class Config:
    openai = OpenAIConfig()
    postgres = DatabaseConfig()
    embedding_api_host = os.getenv("EMBEDDING_API_HOST")


config = Config()
