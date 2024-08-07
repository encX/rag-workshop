FROM python:3 as builder

WORKDIR /app
COPY requirements.txt ./
RUN python -m venv .venv
RUN . .venv/bin/activate
RUN pip install --no-cache-dir -r requirements.txt

COPY common ./common
COPY chatbot ./chatbot

ENTRYPOINT ["fastapi", "run", "chatbot"]
