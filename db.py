"""
Database utilities for pgvector operations.
Handles database connection and vector operations.
"""

import os
import psycopg2
from psycopg2.extras import execute_values


def get_db_connection():
    """
    Create and return a database connection using environment variables.
    """
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")

    conn = psycopg2.connect(database_url)
    return conn


def create_embeddings(text: str):
    """
    Create embeddings for the given text and store in database.

    Args:
        text: Text to create embeddings from

    TODO: Implement the following:
    1. Generate embeddings using OpenAI or Gemini API
    2. Store the text and embeddings in the database
    3. Handle errors appropriately
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # TODO: Generate embeddings using your chosen API
        # Example:
        # embeddings = generate_embeddings_from_api(text)

        # TODO: Insert into database
        # Example:
        # cursor.execute(
        #     "INSERT INTO embeddings (text, vector) VALUES (%s, %s)",
        #     (text, embeddings)
        # )

        conn.commit()
        cursor.close()
    finally:
        conn.close()

    pass


def query_embeddings(query_text: str, limit: int = 5):
    """
    Query similar embeddings from the database.

    Args:
        query_text: Text to query with
        limit: Maximum number of results to return

    Returns:
        List of similar results

    TODO: Implement the following:
    1. Generate embeddings for the query text
    2. Search for similar vectors in the database using pgvector operators
    3. Return the most similar results
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # TODO: Generate embeddings for query
        # query_embeddings = generate_embeddings_from_api(query_text)

        # TODO: Query similar vectors
        # Example using cosine similarity:
        # cursor.execute(
        #     "SELECT text, 1 - (vector <=> %s) AS similarity "
        #     "FROM embeddings "
        #     "ORDER BY vector <=> %s "
        #     "LIMIT %s",
        #     (query_embeddings, query_embeddings, limit)
        # )

        # results = cursor.fetchall()
        results = []

        cursor.close()
        return results
    finally:
        conn.close()
