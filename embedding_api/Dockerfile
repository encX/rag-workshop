FROM python:3

WORKDIR /app
COPY requirements.txt ./
RUN python -m venv .venv
RUN . .venv/bin/activate
RUN pip install --no-cache-dir -r requirements.txt

COPY common ./common
COPY embedding_api ./embedding_api

ENTRYPOINT ["fastapi", "run", "embedding_api"]
