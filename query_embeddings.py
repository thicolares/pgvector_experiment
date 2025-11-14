import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()


def query_embeddings():
    # Connect to PostgreSQL database
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()

    # Perform a similarity search to find documents similar to a given query document.
    query = """
    -- The query first fetches an embeddings vector for the document titled “pgvector”
    -- and then uses the similarity search to get documents with similar content.
    WITH pgv AS (
        SELECT embedding
        FROM document_embeddings JOIN documents USING (id)
        WHERE title = 'pgvector'
    )
    
    -- Note the “<->” operator: that's where all the pgvector magic happens
    -- It's how we get the similarity between two vectors using our HNSW index.
    
    -- <-> - L2 distance (aka Euclidean distance)
    -- See other operators in the pgvector docs: https://github.com/pgvector/pgvector?tab=readme-ov-file#querying
    
    -- The “0.5” is a similarity threshold that will be highly dependent on the
    -- use case and requires fine-tuning in real-world applications.
    -- It means: return all vectors whose distance to the queried vector is less than 0.5
    -- Hence, 0.0 would be a perfect match, and larger values are less similar.
    -- It might depend on the distance metric used, dimensionality of the vectors, and the dataset itself.
    
    SELECT title, content
    FROM document_embeddings
    JOIN documents USING (id)
    WHERE embedding <-> (SELECT embedding FROM pgv) < 0.3;"""
    cur.execute(query)
    # Fetch results
    results = cur.fetchall()
    # Print results in a nice format
    for doc_title, doc_content in results:
        print(f"Document title: {doc_title}")
        print(f"Document text: {doc_content}")
        print()


if __name__ == "__main__":
    query_embeddings()
