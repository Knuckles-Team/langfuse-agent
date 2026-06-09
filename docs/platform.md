# Backing Platform — Langfuse

`langfuse-agent` is a **client** of a [Langfuse](https://langfuse.com/) instance. This
page provides a Docker recipe for deploying one locally to serve as the target of
`LANGFUSE_BASE_URL`. For production topologies, follow the upstream
[Langfuse self-hosting documentation](https://langfuse.com/self-hosting).

!!! note "Backing-system recipe"
    Each connector in the ecosystem follows the same convention — a
    `docs/platform.md` recipe for the system it integrates with, accompanied by a
    sample Compose stack that mirrors [`services/`](https://github.com/Knuckles-Team).
    Systems offered only as a managed service have no local recipe.

## Single-node deployment (Compose)

Langfuse v3 is composed of a web service plus its data plane — PostgreSQL,
ClickHouse, Redis, and an S3-compatible object store (MinIO). The following stack
runs the web service on `:3000`:

```yaml
# docker/langfuse-platform.compose.yml
services:
  langfuse-web:
    image: docker.io/langfuse/langfuse:3
    restart: unless-stopped
    depends_on: [postgres, clickhouse, redis, minio]
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/postgres
      NEXTAUTH_URL: http://localhost:3000
      NEXTAUTH_SECRET: mysecret            # CHANGEME
      SALT: mysalt                          # CHANGEME
      ENCRYPTION_KEY: 0000000000000000000000000000000000000000000000000000000000000000
      CLICKHOUSE_URL: http://clickhouse:8123
      CLICKHOUSE_MIGRATION_URL: clickhouse://clickhouse:9000
      CLICKHOUSE_USER: clickhouse
      CLICKHOUSE_PASSWORD: clickhouse
      REDIS_HOST: redis
      REDIS_PORT: "6379"
      REDIS_AUTH: myredissecret             # CHANGEME
      LANGFUSE_S3_EVENT_UPLOAD_BUCKET: langfuse
      LANGFUSE_S3_EVENT_UPLOAD_ENDPOINT: http://minio:9000
      LANGFUSE_S3_EVENT_UPLOAD_ACCESS_KEY_ID: minio
      LANGFUSE_S3_EVENT_UPLOAD_SECRET_ACCESS_KEY: miniosecret   # CHANGEME
      LANGFUSE_S3_EVENT_UPLOAD_FORCE_PATH_STYLE: "true"

  postgres:
    image: docker.io/postgres:17
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres           # CHANGEME
      POSTGRES_DB: postgres
    volumes: ["langfuse_postgres_data:/var/lib/postgresql/data"]

  clickhouse:
    image: docker.io/clickhouse/clickhouse-server
    environment:
      CLICKHOUSE_USER: clickhouse
      CLICKHOUSE_PASSWORD: clickhouse
    volumes: ["langfuse_clickhouse_data:/var/lib/clickhouse"]

  redis:
    image: docker.io/redis:7
    command: ["--requirepass", "myredissecret"]

  minio:
    image: docker.io/minio/minio
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: minio
      MINIO_ROOT_PASSWORD: miniosecret      # CHANGEME
    volumes: ["langfuse_minio_data:/data"]

volumes:
  langfuse_postgres_data:
  langfuse_clickhouse_data:
  langfuse_minio_data:
```

```bash
docker compose -f docker/langfuse-platform.compose.yml up -d

# Wait for the web service to answer
curl -fsS http://localhost:3000/api/public/health
```

After the web UI is reachable, create an organization and project, then mint a
public/secret API key pair under **Project Settings → API Keys**.

## Connect langfuse-agent

```bash
export LANGFUSE_BASE_URL=http://localhost:3000
export LANGFUSE_PUBLIC_KEY=pk-...
export LANGFUSE_SECRET_KEY=sk-...

langfuse-mcp --transport streamable-http --host 0.0.0.0 --port 8004
```

## Combined deployment

A combined stack places Langfuse and the MCP server on one Docker network, so the
server reaches Langfuse by container name:

```yaml
# docker/stack.compose.yml
services:
  langfuse-web:
    image: docker.io/langfuse/langfuse:3
    ports: ["3000:3000"]
    # …data-plane services as above…

  langfuse-agent-mcp:
    image: knucklessg1/langfuse-agent:latest
    depends_on: [langfuse-web]
    environment:
      - LANGFUSE_BASE_URL=http://langfuse-web:3000
      - LANGFUSE_PUBLIC_KEY=pk-...
      - LANGFUSE_SECRET_KEY=sk-...
      - TRANSPORT=streamable-http
      - HOST=0.0.0.0
      - PORT=8004
    ports: ["8004:8004"]
```

```bash
docker compose -f docker/stack.compose.yml up -d
```

The complete production-grade Langfuse stack used in this ecosystem — with ClickHouse,
Redis, MinIO, and PostgreSQL wired for Docker Swarm — is maintained under
[`services/langfuse/compose.yml`](https://github.com/Knuckles-Team).
