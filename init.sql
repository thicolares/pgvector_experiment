-- Create database
CREATE DATABASE pgvector_experiment;

-- Connect to the database
\c pgvector_experiment

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create a sample table for embeddings
-- TODO: Adjust the vector dimension based on your embedding model
-- OpenAI text-embedding-ada-002: 1536 dimensions
-- OpenAI text-embedding-3-small: 1536 dimensions
-- OpenAI text-embedding-3-large: 3072 dimensions
CREATE TABLE IF NOT EXISTS embeddings (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    vector vector(1536),  -- Adjust dimension as needed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create an index for faster similarity searches
-- Using HNSW (Hierarchical Navigable Small World) algorithm
CREATE INDEX IF NOT EXISTS embeddings_vector_idx ON embeddings 
USING hnsw (vector vector_cosine_ops);

-- TODO: Add your custom initialization queries below
-- Example: Insert sample data, create additional tables, etc.

-- Grant privileges to the application user
GRANT ALL PRIVILEGES ON DATABASE pgvector_experiment TO :POSTGRES_USER;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO :POSTGRES_USER;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO :POSTGRES_USER;
