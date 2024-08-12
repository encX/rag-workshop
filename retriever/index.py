import os
import requests

from common.config import config

DATA_DIR = 'demo/2-products'

def send_files():
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.yaml'):
            file_path = os.path.join(DATA_DIR, filename)
            with open(file_path, 'r') as file:
                content = file.read()
                response = requests.post(f"http://{config.embedding_api_host}/text", json={"source": filename, "text": content})
                print("filename:", filename, "status:", response.status_code)


if __name__ == "__main__":
    send_files()
