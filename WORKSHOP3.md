# Workshop 3: Let's do search

## Step 1: Start dependencies

We still use the same embedding API and its vector database. 

But this time, the vector database is also prepared with embeddings of ~4,000 dummy medical records.

Run the following command to start the API.

```bash
docker compose up -d db embedding-api
```


## Step 2: Start developing search UI

Let's start the search UI with the following command.

```bash
fastapi dev search_web
```

You should have the search UI running at `http://localhost:8000`.


## Step 3: Implement search

In the file `search_web/server.py`, we have a function `search` that renders the search page.
Currently, it only renders the search page with a search bar without searching anything.

Let's modify the `search` function to include the search results. Replace the `embeddings = []` with the code below.

```python
    response_json = requests.get(
        f"http://{config.embedding_api_host}/text?text={term}&top_n=10"
    ).json()
    embeddings = [GetTextResponse(**item) for item in response_json]
```

Now we have the embeddings results. Let's see the search results in the search page.