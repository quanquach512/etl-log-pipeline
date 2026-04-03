#! /bin/bash
set -euo pipefail 

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPT_ROOT="$PROJECT_ROOT/scripts"

echo "[PIPELINE] Starting ETL pipeline...."

bash "$SCRIPT_ROOT/download.sh"
bash "$SCRIPT_ROOT/extract.sh"
"$PROJECT_ROOT/venv/bin/python" "$SCRIPT_ROOT/transform.py"
"$PROJECT_ROOT/venv/bin/python" "$SCRIPT_ROOT/load.py"

echo "[PIPELINE] ETL pipeline completed..."