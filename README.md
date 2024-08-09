# RAG Workshop

This project is the boilerplate for the **"Build your own AI-powered internal search engine"** workshop for **TechSauce Global Summit 2024** on 8th August 2024.

This workshop's audience is developers who have never worked with AI/LLM before. The goal is to introduce the concept of how LLM works, RAG (Retrieval-Augmented Generation), Embeddings. And build a simple search engine and a chatbot using these concepts.

## Project Structure

There are 4 main components in this project:

- **Embedding API** - A simple REST API to save text and retrieve text relevant to the input query. Hiding the complexity of embeddings and vector manipulation.
- **Search UI** - A simple search engine UI to search for text using the Embedding API.
- **Chatbot UI** - A simple chatbot UI to chat with information retrieved via the Embedding API.
- **Retriever** - A simple script to scan knowledge base and save the text to the Embedding API.

![Project Structure](docs/diagram.png)

This workshop primaliry uses OpenAI services, so you need to have an OpenAI account and API key to run this project. But feel free to update the code (`common/llm.py`) to use any other provider.

## Setup

This project uses `python >= 3.11`. To setup the project, run the following commands:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

This will create a virtual environment in the `.venv` directory, activate it, and install the dependencies listed in `requirements.txt`.

> If you are not familiar with developing python projects, virtual environment is a way to isolate the dependencies of a project from the system dependencies. This way, you can have different versions of the same package in different projects without any conflict. Read more about it [here](https://docs.python.org/3/library/venv.html).

> Virtual environment is activated per shell session. So, you need to run `source .venv/bin/activate` everytime you open a new terminal.


## [Then, checkout wiki for workshop handbook](https://github.com/encX/rag-workshop/wiki)
