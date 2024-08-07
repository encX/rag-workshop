import numpy as np
import psycopg

from pgvector.psycopg import register_vector
from typing import List

from common.config import config
from common.models import TextEmbedding


class Storage:
    def __init__(self):
        with psycopg.connect(config.postgres.connection_string) as conn:
            conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS embedding (
                    id SERIAL PRIMARY KEY,
                    text TEXT NOT NULL,
                    source TEXT NOT NULL,
                    vector vector(1536) NOT NULL
                )
                """
            )

    def save_embedding(self, embedding: TextEmbedding) -> int:
        with psycopg.connect(config.postgres.connection_string) as conn:
            register_vector(conn)
            vector = np.array(embedding.vector)
            cur = conn.execute(
                "INSERT INTO embedding (text, source, vector) VALUES (%s, %s, %s) RETURNING id",
                (embedding.text, embedding.source, vector),
            )
            return cur.fetchone()[0]

    def get_most_similar(
        self, embedding: TextEmbedding, n=1, distance_limit=0.8
    ) -> List[TextEmbedding]:
        with psycopg.connect(config.postgres.connection_string) as conn:
            register_vector(conn)
            vector = np.array(embedding.vector)
            cur = conn.execute(
                "WITH dist as (SELECT text, source, vector, vector <=> %s as distance FROM embedding)"
                "SELECT text, source, vector, distance FROM dist WHERE distance <= %s ORDER BY distance LIMIT %s",
                (vector, distance_limit, n),
            )
            return [
                TextEmbedding(
                    text=text, source=source, vector=vector, distance=distance
                )
                for text, source, vector, distance in cur.fetchall()
            ]
