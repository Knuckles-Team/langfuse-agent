# syntax=docker/dockerfile:1
# Two right-sized published images plus one exact offline release image come from
# ONE Dockerfile, selected by build --target. Each is slim multi-stage (build in a
# builder, ship only /usr/local — no dev-tools/source):
#
#   --target agent  (DEFAULT)  installs langfuse-agent[agent] = the FULL runtime
#                              (agent-utilities[agent-runtime]: pydantic-ai + skills;
#                              the full epistemic-graph engine is a base dependency).
#                              The provider's [agent] also includes [mcp], so this image
#                              can run EITHER the agent OR the mcp server. Push as the
#                              default tags: latest / main / <version>.
#
#   --target mcp               installs langfuse-agent[mcp]   = MCP-server tooling ONLY
#                              (agent-utilities[mcp]: FastMCP/FastAPI plus the mandatory
#                              full epistemic-graph base runtime). It omits the optional
#                              provider agent/frontends. Push as the :mcp / :mcp-<version> tag.
#
#   docker build --target agent -t langfuse-agent:local .
#   docker build --target mcp   -t langfuse-agent:mcp    .
#   docker build --target mcp-local \
#     --build-arg RELEASE_REQUIREMENTS=langfuse-agent-requirements.txt \
#     --build-arg RELEASE_REQUIREMENTS_SHA256=<requirements-sha256> \
#     --build-arg AGENT_UTILITIES_VERSION=<exact-version> \
#     --build-arg EPISTEMIC_GRAPH_VERSION=<exact-version> \
#     --build-arg LANGFUSE_AGENT_VERSION=<exact-version> .
FROM python:3.14-slim@sha256:cea0e6040540fb2b965b6e7fb5ffa00871e632eef63719f0ea54bca189ce14a6 AS builder-base
COPY --from=ghcr.io/astral-sh/uv:0.11.7@sha256:240fb85ab0f263ef12f492d8476aa3a2e4e1e333f7d67fbdd923d00a506a516a /uv /uvx /bin/
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_SYSTEM_PYTHON=1 \
    UV_HTTP_TIMEOUT=3600

FROM builder-base AS builder-published
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

# Slim MCP-only dependency closure.
FROM builder-published AS builder-mcp
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system --break-system-packages langfuse-agent[mcp]==1.0.3

# Full agent runtime dependency closure.
FROM builder-published AS builder-agent
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system --break-system-packages langfuse-agent[agent]==1.0.3

# Exact offline release input for the MCP provider runtime. The caller supplies one
# complete, hash-locked wheel closure for Langfuse Agent MCP, Agent Utilities MCP, and
# the full Epistemic Graph runtime. Source distributions and local-source metadata are
# rejected.
FROM builder-base AS builder-mcp-local
ARG RELEASE_REQUIREMENTS=langfuse-agent-requirements.txt
ARG RELEASE_REQUIREMENTS_SHA256
ARG AGENT_UTILITIES_VERSION
ARG EPISTEMIC_GRAPH_VERSION
ARG LANGFUSE_AGENT_VERSION
COPY release-wheelhouse/ /tmp/release-wheelhouse/
RUN test "$(basename -- "${RELEASE_REQUIREMENTS}")" = "${RELEASE_REQUIREMENTS}" \
    && case "${RELEASE_REQUIREMENTS}" in *.txt) ;; *) exit 64 ;; esac \
    && test -n "${AGENT_UTILITIES_VERSION}" \
    && test -n "${EPISTEMIC_GRAPH_VERSION}" \
    && test -n "${LANGFUSE_AGENT_VERSION}" \
    && printf '%s  %s\n' "${RELEASE_REQUIREMENTS_SHA256}" "/tmp/release-wheelhouse/${RELEASE_REQUIREMENTS}" \
        | sha256sum --check --strict - \
    && uv pip install --system --break-system-packages --offline --no-index \
        --find-links /tmp/release-wheelhouse --only-binary :all: --require-hashes \
        --requirement "/tmp/release-wheelhouse/${RELEASE_REQUIREMENTS}" \
    && python -c 'import importlib.metadata as m, pathlib, shutil, sys; au, eg, lf = sys.argv[1:]; assert sys.version_info[:2] == (3, 12); assert m.version("agent-utilities") == au; assert m.version("epistemic-graph") == eg; assert m.version("langfuse-agent") == lf; assert shutil.which("graph-os") and shutil.which("langfuse-mcp"); roots = {pathlib.Path(d.locate_file("")) for d in m.distributions()}; assert not any(path for root in roots for path in root.glob("*.dist-info/direct_url.json")); import epistemic_graph.numeric' \
        "${AGENT_UTILITIES_VERSION}" "${EPISTEMIC_GRAPH_VERSION}" "${LANGFUSE_AGENT_VERSION}"

FROM python:3.14-slim@sha256:cea0e6040540fb2b965b6e7fb5ffa00871e632eef63719f0ea54bca189ce14a6 AS runtime-base
ARG HOST=127.0.0.1
ARG PORT=8000
ARG TRANSPORT="stdio"
ARG AUTH_TYPE="none"
ENV HOST=${HOST} \
    PORT=${PORT} \
    TRANSPORT=${TRANSPORT} \
    AUTH_TYPE=${AUTH_TYPE} \
    PYTHONUNBUFFERED=1 \
    PATH="/usr/local/bin:${PATH}" \
    UV_HTTP_TIMEOUT=3600 \
    UV_SYSTEM_PYTHON=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Slim image: MCP server only.
# Fixed identity for least-privilege runtime and stable volume ownership.
RUN groupadd --system --gid 10001 app \
    && useradd --system --uid 10001 --gid 10001 --no-create-home \
        --home-dir /tmp --shell /usr/sbin/nologin app
ENV HOME=/tmp \
    XDG_CONFIG_HOME=/tmp/.config \
    XDG_CACHE_HOME=/tmp/.cache

FROM runtime-base AS mcp
USER 10001:10001
COPY --from=builder-mcp /usr/local /usr/local
CMD ["langfuse-mcp"]

# Exact MCP release target: only the closed wheelhouse reaches this image.
FROM runtime-base AS mcp-local
USER 10001:10001
COPY --from=builder-mcp-local /usr/local /usr/local
CMD ["langfuse-mcp"]

# Full image (DEFAULT target): agent runtime; can also run the mcp server.
FROM runtime-base AS agent
USER 10001:10001
COPY --from=builder-agent /usr/local /usr/local
CMD ["langfuse-agent"]
