#!/bin/bash

# Navigate to the workspace directory
cd /Users/d-23-9386/Desktop/ELTWarehouse

# Ensure logs directory exists
mkdir -p logs

echo "============================================================"
echo "  Starting Full Project Stack"
echo "============================================================"

# ── Step 0: Kill any stale servers from a previous run ───────────────────────
echo ""
echo "[0/4] Cleaning up any previously running servers..."

STALE_PIDS=$(lsof -ti :8501,:8080 2>/dev/null)
if [ -n "$STALE_PIDS" ]; then
    echo "      Found stale processes on ports 8080/8501 (PIDs: $STALE_PIDS). Stopping them..."
    kill $STALE_PIDS 2>/dev/null
    sleep 2   # Give them time to release the DuckDB file lock
    echo "      Stale processes stopped."
else
    echo "      No stale processes found."
fi

# ── Step 1: Run the ELT pipeline (must finish before servers start) ───────────
echo ""
echo "[1/4] Running ELT Pipeline..."
./venv/bin/python run_pipeline.py
if [ $? -ne 0 ]; then
    echo ""
    echo "  ❌  Pipeline execution FAILED. Aborting startup."
    echo "      Check logs/pipeline.log for details."
    exit 1
fi
echo "  ✅  Pipeline completed successfully."

# ── Step 2: Generate dbt Docs ─────────────────────────────────────────────────
echo ""
echo "[2/4] Generating dbt Documentation..."
./venv/bin/dbt docs generate --project-dir ecommerce_dbt > logs/dbt_docs.log 2>&1
if [ $? -ne 0 ]; then
    echo "  ⚠️   dbt docs generation failed (see logs/dbt_docs.log). Continuing..."
else
    echo "  ✅  dbt docs generated."
fi

# ── Step 3: Start dbt Docs Server in background ───────────────────────────────
echo ""
echo "[3/4] Starting dbt Docs Server (port 8080)..."
./venv/bin/dbt docs serve --project-dir ecommerce_dbt --port 8080 >> logs/dbt_docs.log 2>&1 &
DBT_DOCS_PID=$!

# Brief wait to let the server bind its port
sleep 2

# ── Step 4: Start Streamlit Dashboard in background ───────────────────────────
echo ""
echo "[4/4] Starting Streamlit Dashboard (port 8501)..."
./venv/bin/streamlit run dashboard/app.py > logs/streamlit.log 2>&1 &
STREAMLIT_PID=$!

# Brief wait to confirm Streamlit started
sleep 2

# Open both URLs in the default browser
open http://localhost:8080 2>/dev/null || true
open http://localhost:8501 2>/dev/null || true

echo ""
echo "============================================================"
echo "  ✅  Project Stack Launched Successfully!"
echo "============================================================"
echo "  📊  Streamlit Dashboard : http://localhost:8501"
echo "  📖  dbt Docs            : http://localhost:8080"
echo ""
echo "  Background Process PIDs:"
echo "  - dbt Docs Server PID  : $DBT_DOCS_PID"
echo "  - Streamlit Server PID : $STREAMLIT_PID"
echo ""
echo "  Logs:"
echo "  - Pipeline  : logs/pipeline.log"
echo "  - Streamlit : logs/streamlit.log"
echo "  - dbt Docs  : logs/dbt_docs.log"
echo ""
echo "  To stop all servers, run:"
echo "  kill $DBT_DOCS_PID $STREAMLIT_PID"
echo "============================================================"
