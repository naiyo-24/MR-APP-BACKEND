#!/bin/sh
set -e

echo "🚀 Container starting..."

# -------------------------------
# Wait for database
# -------------------------------
echo "⏳ Waiting for database to be ready..."

RETRIES=30
until python - <<'PY'
import os, sys
from sqlalchemy import create_engine

db_url = os.getenv("DATABASE_URL")
if not db_url:
    sys.exit(1)

try:
    engine = create_engine(db_url)
    with engine.connect() as conn:
        pass
except Exception:
    sys.exit(1)

sys.exit(0)
PY
do
  RETRIES=$((RETRIES-1))
  if [ "$RETRIES" -le 0 ]; then
    echo "❌ Database not available"
    exit 1
  fi
  sleep 1
done

echo "✅ Database is ready"

# -------------------------------
# Migration mode
# -------------------------------
if [ "$RUN_MIGRATIONS" = "true" ]; then
  echo "📦 Running Alembic migrations..."
  alembic upgrade head
  echo "✅ Migrations completed. Exiting."
  exit 0
fi

# -------------------------------
# Backend mode
# -------------------------------
echo "🟢 Starting FastAPI server..."
exec uvicorn main:app --host 0.0.0.0 --port 2000
