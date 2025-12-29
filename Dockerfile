FROM python:3.11-slim

# Set the working directory
WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

# Install requirements and Alembic
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install alembic

COPY . .

EXPOSE 2000


# Entrypoint script to run Alembic migrations before starting the app
COPY ./alembic ./alembic
COPY ./alembic.ini ./alembic.ini
COPY ./models ./models
COPY ./db.py ./db.py
COPY ./main.py ./main.py

ENV PYTHONPATH="/app"

ENTRYPOINT ["/bin/sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 2000"]
