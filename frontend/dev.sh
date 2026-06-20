#!/usr/bin/env bash
# RedOps Console — one-command dev launcher (Linux / WSL).
#
# Usage:
#   cd frontend && ./dev.sh
#
# Starts the Vite dev server. Make sure the backend is running separately
# (cd backend && uvicorn app.main:app --reload).
set -euo pipefail

cd "$(dirname "$0")"

# Detect WSL and enable polling-based file watching for projects on /mnt/c.
if grep -qiE "(microsoft|wsl)" /proc/version 2>/dev/null; then
  echo "→ WSL detected: enabling polling file-watch (HMR on the Windows drive)."
  export VITE_USE_POLLING=true
fi

if ! command -v node >/dev/null 2>&1; then
  echo "✗ Node.js not found."
  echo "  Install Node 18+ in your Linux/WSL environment, e.g.:"
  echo "    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash"
  echo "    exec \$SHELL && nvm install 20"
  exit 1
fi

echo "→ Node $(node --version), npm $(npm --version)"

if [ ! -f .env ]; then
  cp .env.example .env
  echo "→ Created .env from .env.example"
fi

if [ ! -d node_modules ]; then
  echo "→ Installing dependencies (first run)…"
  npm install
fi

echo "→ Starting Vite on http://localhost:5173  (Ctrl+C to stop)"
echo "  API proxied to ${VITE_API_TARGET:-http://localhost:8000}"
exec npm run dev
