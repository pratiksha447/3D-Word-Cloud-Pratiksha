#!/usr/bin/env bash
set -e

echo "==> Setting up backend (FastAPI)..."
cd backend

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "==> Starting backend on http://localhost:8000 ..."
uvicorn app:app --reload --port 8000 &
BACKEND_PID=$!

cd ../frontend

echo "==> Installing frontend dependencies..."
npm install

echo "==> Starting frontend on http://localhost:5173 ..."
npm run dev &
FRONTEND_PID=$!

echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo "Both servers are running. Press Ctrl+C to stop."

wait $BACKEND_PID $FRONTEND_PID
