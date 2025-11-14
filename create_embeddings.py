from openai import OpenAI
from google import genai
from google.genai import types

import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


def create_embedding(doc_content, service="openai"):
    if service == "openai":
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Pick the embedding model
        model_id = "text-embedding-ada-002"

        response = client.embeddings.create(input=doc_content, model=model_id)

        return response["data"][0]["embedding"]

    if service == "gemini":
        # The client gets the API key from the environment variable `GEMINI_API_KEY`.
        # https://ai.google.dev/gemini-api/docs/quickstart#make-first-request

        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

        # Pick the embedding model
        model_id = "gemini-embedding-001"

        result = client.models.embed_content(
            model=model_id,
            contents=doc_content,
            config=types.EmbedContentConfig(output_dimensionality=1536),
        )
        
        return result.embeddings[0].values

    raise ValueError(f"Unsupported service: {service}")


def create_embeddings():
    # Load OpenAI API key

    # Connect to PostgreSQL database
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))

    # Fetch documents from the database
    cur = conn.cursor()
    cur.execute("SELECT id, content FROM documents")
    documents = cur.fetchall()
    
    embedding_service = psycopg2.connect(os.getenv("EMBEDDING_SERVICE"))

    # Process and store embeddings in the database
    for doc_id, doc_content in documents:
        embedding = create_embedding(doc_content, embedding_service)
        cur.execute(
            "INSERT INTO document_embeddings (id, embedding) VALUES (%s, %s);",
            (doc_id, embedding),
        )
        conn.commit()
    # Commit and close the database connection
    conn.commit()


if __name__ == "__main__":
    create_embeddings()
