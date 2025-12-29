FROM python:3.11-slim

# Set working directory
WORKDIR /app

# System dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install alembic psycopg[binary]

# Copy application code
COPY . .

# Copy entrypoint
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Environment
ENV PYTHONPATH="/app"

EXPOSE 2000

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
