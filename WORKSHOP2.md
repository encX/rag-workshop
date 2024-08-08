# Workshop 2: Let's build plug an embedding to the chatbot

## Step 1: Start depednencies

We already have the embedding API and its vector database prepared for you. Run the following command to start the API.

```bash
docker compose up -d db embedding-api
```

> Let's test the embedding API by browsing to `http://localhost:8001/`. You should see the API documentation.


## Step 2: Start developing chatbot

Let's start chatbot the same command as before.

```bash
fastapi dev chatbot
```

You should have the chatbot running at `http://localhost:8000`.


## Step 3: Plug the embedding API to the chatbot

In the file `chatbot/server.py`, we have a function `chat` that respond to the user input.
Currently, it only send the conversation messages directly to OpenAI to get the next "assistant" message.

Let's modify at the `### Add embedding API call here ###`. Replace this text with the code below.

```python
    response_json = requests.get(
        f"http://{config.embedding_api_host}/text?text={last_message}&top_n=3"
    ).json()
    embeddings = [GetTextResponse(**item) for item in response_json]
```

Now we have the embeddings of the last message. Let's pass it to generate the system message.
On the line of `system_message = __get_system_message()`, update as below.

```python
    system_message = __get_system_message(embeddings)
```

Finally, let's modify the `__get_system_message` function at the bottom of the file to include the embeddings in the system message.

```python
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
```

The chatbot should automatically reload with the new changes. 
Try asking 
```
recommend me a fragrance
```
And see the chatbot response.


## Step 4: Add knowledge to the system

The embeddings API is currently empty. Let's add some knowledge to it.

Browse to `http://localhost:8001/docs` and try run the "Save Text" endpoint with the following data, one by one.

```json
{
  "text": "title: Essence Mascara Lash Princess // description: The Essence Mascara Lash Princess is a popular mascara known for its volumizing and lengthening effects. Achieve dramatic lashes with this long-lasting and cruelty-free formula. // category: beauty // price: 9.99 // discountPercentage: 7.17",
  "source": "Product 1"
}
```

```json
{
  "text": "title: Eyeshadow Palette with Mirror // description: The Eyeshadow Palette with Mirror offers a versatile range of eyeshadow shades for creating stunning eye looks. With a built-in mirror, it's convenient for on-the-go makeup application. // category: beauty // price: 19.99",
  "source": "Product 2"
}
```

```json
{
  "text": "title: Dolce Shine Eau de // description: Dolce Shine by Dolce & Gabbana is a vibrant and fruity fragrance, featuring notes of mango, jasmine, and blonde woods. It's a joyful and youthful scent. // category: fragrances // price: 69.99 // discountPercentage: 11.47",
  "source": "Product 3"
}
```

```json
{
  "text": "title: Chanel Coco Noir Eau De // description: Coco Noir by Chanel is an elegant and mysterious fragrance, featuring notes of grapefruit, rose, and sandalwood. Perfect for evening occasions. // category: fragrances // price: 129.99 // discountPercentage: 18.64",
  "source": "Product 4"
}
```

## Step 5: Retrieve the knowledge

Now, try asking the chatbot again.

```
recommend me a fragrance
```

You should now see the product information in the chatbot response.
