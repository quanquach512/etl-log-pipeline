#! /bin/bash
set -e 

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RAW_DIR="$PROJECT_ROOT/data/raw"
LOG_FILE="$RAW_DIR/access.log"

URL="https://ita.ee.lbl.gov/traces/NASA_access_log_Jul95.gz"
ARCHIVE_FILE="$RAW_DIR/NASA_access_log_Jul95.gz"

mkdir -p "$RAW_DIR"

echo "[DOWNLOAD] Downloading dataset..."
curl -L -o "$ARCHIVE_FILE" "$URL"

echo "[DOWNLOAD] Extracting archive..."
gunzip -c "$ARCHIVE_FILE" > "$LOG_FILE"

echo "[DOWNLOAD] Done! Saved to $LOG_FILE"


