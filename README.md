
<div align="center">
    <img src="pgvector_experiment.png" alt="pgvector Experiment Logo" width="200" height="200">
</div>




# `pgvector` Experiment

A simple PostgreSQL [`pgvector`](https://github.com/pgvector/pgvector) experiment project for creating and querying vector embeddings using OpenAI or Google Gemini APIs.

## Prerequisites

Ensure you have the following installed on your machine:

- **Docker** (version 20.10 or higher) with **Docker Compose** plugin

## Quick Start

### 1. Clone and Setup

```bash
git clone git@github.com:thicolares/pgvector_experiment.git
cd pgvector_experiment
```

### 2. Configure Environment Variables

Copy the example environment file and update it with your API keys:

```bash
cp .env.example .env
```

Edit the `.env` file and add your API keys:

```bash
# Required: Add your OpenAI API key
OPENAI_API_KEY=sk-your-actual-openai-api-key

# Required: Add your Gemini API key
GEMINI_API_KEY=your-actual-gemini-api-key

# Optional: Customize PostgreSQL credentials (defaults provided)
POSTGRES_USER=pgvector_user
POSTGRES_PASSWORD=pgvector_password
POSTGRES_PORT=5432
```

### 3. Start the Services

Build and start the Docker containers:

```bash
docker compose up -d --build
```

This will:
- Build a PostgreSQL container with pgvector extension
- Build a Python container with `uv` package manager
- Create the `pgvector_experiment` database
- Set up persistent storage for PostgreSQL data

### 4. Verify Services are Running

```bash
docker compose ps
```

You should see both `pgvector_postgres` and `pgvector_python` containers running.

## Usage

### Running Commands Inside the Container

Execute Python scripts inside the container:

```bash
# Create embeddings
docker compose exec python uv run main.py create --text "Your text here"

# Query embeddings
docker compose exec python uv run main.py query --text "Search query" --limit 5
```

### Running Commands from Host Machine

If you want to run commands directly on your host machine (after installing dependencies locally):

```bash
# Install dependencies with uv
uv pip install -r pyproject.toml

# Create embeddings
uv run main.py create --text "Your text here"

# Query embeddings
uv run main.py query --text "Search query" --limit 5
```

## Accessing PostgreSQL Database

### From Host Machine

You can connect to the PostgreSQL database from your host machine using any PostgreSQL client:

**Connection Details:**
- **Host:** `localhost`
- **Port:** `5432` (or the value of `POSTGRES_PORT` in your `.env` file)
- **Database:** `pgvector_experiment`
- **Username:** `pgvector_user` (or the value of `POSTGRES_USER`)
- **Password:** `pgvector_password` (or the value of `POSTGRES_PASSWORD`)

**Using psql command line:**

```bash
psql -h localhost -p 5432 -U pgvector_user -d pgvector_experiment
```

**Connection String:**

```
postgresql://pgvector_user:pgvector_password@localhost:5432/pgvector_experiment
```

### From Inside Docker Network

Other containers in the same Docker network can connect using:

```
postgresql://pgvector_user:pgvector_password@postgres:5432/pgvector_experiment
```



## Development

### Editing Code

Edit files on your host machine. Changes are immediately available in the container via volume mounting.

### Installing New Dependencies

1. Add the dependency to `pyproject.toml`
2. Rebuild the Python container:

```bash
docker compose up -d --build python
```

Or install inside the running container:

```bash
docker compose exec python uv pip install package-name
```

### Viewing Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f postgres
docker compose logs -f python
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

### Modify Vector Dimensions

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

### Add Custom SQL Initialization

Edit `init.sql` to add your custom tables, indexes, or seed data.

## Cleanup

### Stop Services

```bash
docker compose down
```

### Remove All Data (including volumes)

```bash
docker compose down -v
```

### Remove All Images

```bash
docker compose down --rmi all -v
```

## Resources

- [pgvector Documentation](https://github.com/pgvector/pgvector)
- [OpenAI Embeddings API](https://platform.openai.com/docs/guides/embeddings)
- [Google Gemini API](https://ai.google.dev/docs)

## License

This is an experimental project for educational purposes.
