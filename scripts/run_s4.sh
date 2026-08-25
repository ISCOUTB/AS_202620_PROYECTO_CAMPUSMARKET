#!/usr/bin/env bash
set -euo pipefail

python -m uvicorn backend.app.main:app --reload --port 8000 &
BACKEND_PID=$!

cleanup() {
  kill "$BACKEND_PID" 2>/dev/null || true
}
trap cleanup EXIT

cd frontend/campusmarket
flutter pub get
flutter run -d chrome --web-port 3000
