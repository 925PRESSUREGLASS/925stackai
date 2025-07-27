#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# run_all.sh – One-shot local dev launcher (Linux, macOS, WSL)                #
###############################################################################
# Stages: 1) Python venv + deps  2) Rebuild vector index                      #
#         3) Docker stack up  4) Run tests  5) Wait & open Streamlit GUI      #
###############################################################################

# ---------- 1. Python env & deps --------------------------------------------
if [ ! -d ".venv" ]; then
  python -m venv .venv
fi
source .venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q

# ---------- 2. Rebuild vector index -----------------------------------------
python scripts/rebuild_index.py \
       --input ./docs \
       --store ./memory/vector_store

# ---------- 3. Docker Compose stack -----------------------------------------
docker compose --env-file .env up --build -d

# ---------- 4. Run tests -----------------------------------------------------
pytest -q

# ---------- 5. Wait for Streamlit GUI & open ---------------------------------
python scripts/helper/wait_on_port.py 8501
# xdg-open (Linux), open (macOS), start (fallback Windows shell in WSL)
xdg-open http://localhost:8501 2>/dev/null || \
open http://localhost:8501 2>/dev/null || \
start http://localhost:8501

echo "✅ 925stackai is up and running."
