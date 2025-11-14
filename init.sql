-- Database pgvector_experiment is automatically created by POSTGRES_DB env var

-- Enable pgvector extension
-- This command stores the vector extension metadata in the database,
-- like data types and functions definitions and C code references.
CREATE EXTENSION IF NOT EXISTS vector;

-- Create a sample table for documents
CREATE TABLE IF NOT EXISTS documents (
    id int PRIMARY KEY,
    title text NOT NULL,
    content TEXT NOT NULL
);

-- Create document_embeddings table
-- TODO: Adjust the vector dimension based on your embedding model
-- OpenAI text-embedding-ada-002: 1536 dimensions
-- OpenAI text-embedding-3-small: 1536 dimensions
-- OpenAI text-embedding-3-large: 3072 dimensions
CREATE TABLE IF NOT EXISTS document_embeddings (
    id int PRIMARY KEY,
    embedding vector(1536) NOT NULL -- Adjust dimension as needed
);

-- Let’s index our data using the HNSW index
-- Using HNSW (Hierarchical Navigable Small World) algorithm
-- Records that this index uses hnsw + vector_l2_ops
-- Stores metadata in pg_index and pg_class
CREATE INDEX IF NOT EXISTS document_embeddings_embedding_idx ON document_embeddings
USING hnsw (embedding vector_l2_ops);

-- Insert documents into documents table
INSERT INTO documents VALUES ('1', 'pgvector', 'pgvector is a PostgreSQL extension that provides support for vector similarity search and nearest neighbor search in SQL.');
INSERT INTO documents VALUES ('2', 'pg_similarity', 'pg_similarity is a PostgreSQL extension that provides similarity and distance operators for vector columns.');
INSERT INTO documents VALUES ('3', 'pg_trgm', 'pg_trgm is a PostgreSQL extension that provides functions and operators for determining the similarity of alphanumeric text based on trigram matching.');
INSERT INTO documents VALUES ('4', 'pg_prewarm', 'pg_prewarm is a PostgreSQL extension that provides functions for prewarming relation data into the PostgreSQL buffer cache.');

