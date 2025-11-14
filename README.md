
<div align="center">
    <img src="pgvector_experiment.png" alt="pgvector Experiment Logo" width="200" height="200">
</div>

# `pgvector` Experiment

A simple PostgreSQL [`pgvector`](https://github.com/pgvector/pgvector) experiment project for storing and querying vector embeddings created using OpenAI or Google Gemini.

## Prerequisites

Ensure you have the following installed on your machine:

- **Docker** (version 20.10 or higher) with **Docker Compose** plugin

## Quick start

### 1. Clone and setup

```bash
git clone git@github.com:thicolares/pgvector_experiment.git
cd pgvector_experiment
```

### 2. Configure environment variables

Copy the example environment file and update it with your API keys:

```bash
cp .env.example .env
```

Edit the `.env` file and add your API keys.

### 3. Start the services

Build and start the Docker containers:

```bash
docker compose up -d --build
```

This will:
- Build and run PostgreSQL with pgvector and Python with `uv`
- Create the database, install pgvector extension, and initialize mock documents (see `init.sql`)

## Usage

### 1. Create embeddings by running

```
docker compose exec python uv run create_embeddings.py                      
```

For each document, this generates embeddings via external APIs and stores them as `pgvector` vectors in PostgreSQL.

Expected default output:
```
Processed document ID: 1
Processed document ID: 2
Processed document ID: 3
Processed document ID: 4
Committing changes to the database...
```

### 2. Query similar documents by running

```
 docker compose exec python uv run query_similar_documents.py --threshold 0.5
```

This retrieves documents with embeddings similar to a sample embedding stored in the database. The `--threshold` parameter controls similarity sensitivity (lower = more similar). 0.0 is exact match, 1.0 is very dissimilar. Default is 0.5.

Expected default output:
```
Using similarity threshold: 0.5
(Change with --threshold X, default 0.5)

Document title: pgvector
Document text: pgvector is a PostgreSQL extension that provides support for vector similarity search and nearest neighbor search in SQL.

Document title: pg_similarity
Document text: pg_similarity is a PostgreSQL extension that provides similarity and distance operators for vector columns.

Document title: pg_trgm
Document text: pg_trgm is a PostgreSQL extension that provides functions and operators for determining the similarity of alphanumeric text based on trigram matching.

```

## Accessing PostgreSQL database

### From host machine

You can connect to the PostgreSQL database from your host machine using any PostgreSQL client:

**Connection Details:**
- **Host:** `0.0.0.0`
- **Port:** `5433` (or the value of `POSTGRES_PORT` in your `.env` file)
- **Database:** `pgvector_experiment`
- **Username:** `pgvector_user` (or the value of `POSTGRES_USER`)
- **Password:** `pgvector_password` (or the value of `POSTGRES_PASSWORD`)

**Using psql command line:**

```bash
psql -h 0.0.0.0 -p 5433 -U pgvector_user -d pgvector_experiment
```

## Development

### Editing code

Edit files on your host machine. Changes are immediately available in the container via volume mounting.

### Installing new dependencies

1. Add the dependency to `pyproject.toml`
2. Rebuild the Python container:

```bash
docker compose up -d --build python
```

Or install inside the running container (ephemeral):

```bash
docker compose exec python uv pip install package-name
```

### Viewing logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f postgres
docker compose logs -f python
```

### Fresh start

```bash
docker compose down -v
docker compose build --no-cache
docker compose up -d --build
```

### Verify services are running

```bash
docker compose ps                                                           
NAME                IMAGE                          COMMAND                  SERVICE    CREATED          STATUS                    PORTS
pgvector_postgres   pgvector_experiment-postgres   "docker-entrypoint.s…"   postgres   20 minutes ago   Up 20 minutes (healthy)   0.0.0.0:5433->5432/tcp
pgvector_python     pgvector_experiment-python     "tail -f /dev/null"      python     20 minutes ago   Up 19 minutes  
```

## Contributing

Want to contribute? Great! Here's a quick flow to get started:

1. **Fork the repository** - Create your own copy
2. **Clone your fork** - `git clone git@github.com:YOUR-USERNAME/pgvector_experiment.git`
3. **Create a branch** - `git checkout -b feature/your-feature-name`
4. **Make your changes** - Edit, test, and commit your work
5. **Push to your fork** - `git push origin feature/your-feature-name`
6. **Open a Pull Request** - Submit your changes for review

For a detailed guide on contributing to GitHub projects, see the [GitHub Contributing Guide](https://docs.github.com/en/get-started/exploring-projects-on-github/contributing-to-a-project).


## Customization

### Modify vector dimensions

The default vector dimension is set to 1536 (OpenAI's embedding size). To change this:

1. Edit `init.sql` and change the vector dimension:
   ```sql
   vector vector(1536)  -- Change 1536 to your desired dimension
   ```

2. Rebuild the database:
   ```bash
   docker compose down -v  # WARNING: This deletes all data
   docker compose up -d --build
   ```

### Add custom SQL initialization

Edit `init.sql` to add your custom tables, indexes, or seed data.

## Cleanup

### Stop services

```bash
docker compose down
```

### Remove all data (including volumes)

```bash
docker compose down -v
```

### Remove all images

```bash
docker compose down --rmi all -v
```

## Resources

- Code inspired by [What is pgvector, and How Can It Help Your Vector Database?](https://www.enterprisedb.com/blog/what-is-pgvector)
- [pgvector Documentation](https://github.com/pgvector/pgvector)
- [OpenAI Embeddings API](https://platform.openai.com/docs/guides/embeddings)
- [Google Gemini API](https://ai.google.dev/docs)

## License

This is an experimental project for educational purposes.