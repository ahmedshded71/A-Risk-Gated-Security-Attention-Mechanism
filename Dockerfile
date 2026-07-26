# ==============================================================================
# RGSA-Transformer v5.6.2 - Docker Image (CPU)
# Risk-Gated Security Attention Mechanism for Real-Time IDS
# ==============================================================================

# ------------------ Stage 1: Builder ------------------
FROM python:3.12-slim AS builder

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv (fast Python package manager)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /build

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install dependencies
RUN uv sync --frozen --no-dev --no-install-project

# ------------------ Stage 2: Runtime ------------------
FROM python:3.12-slim AS runtime

LABEL maintainer="Eslam Fouda, Ahmed Saad"
LABEL version="5.6.2"
LABEL description="RGSA-Transformer: Risk-Gated Security Attention for IDS"

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy uv from builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Create non-root user
RUN groupadd -r rgsa && useradd -r -g rgsa -m rgsa

# Set working directory
WORKDIR /app

# Copy virtual environment
COPY --from=builder --chown=rgsa:rgsa /build/.venv /app/.venv

# Copy application code
COPY --chown=rgsa:rgsa src/ /app/src/
COPY --chown=rgsa:rgsa main.py /app/
COPY --chown=rgsa:rgsa README.md /app/
COPY --chown=rgsa:rgsa scripts/ /app/scripts/

# Make scripts executable
RUN chmod +x /app/scripts/*.sh 2>/dev/null || true

# Create directories
RUN mkdir -p /app/data /app/outputs \
    && chown -R rgsa:rgsa /app/data /app/outputs

# Environment variables
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app/src:$PYTHONPATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TF_CPP_MIN_LOG_LEVEL=2 \
    MPLBACKEND=Agg \
    OMP_NUM_THREADS=4

# Switch to non-root user
USER rgsa

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import rgsa; print(rgsa.__version__)" || exit 1

# Default command
CMD ["python", "main.py"]