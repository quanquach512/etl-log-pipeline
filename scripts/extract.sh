#! /bin/bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RAW_DIR="$PROJECT_ROOT/data/raw"
PROCESSED_DIR="$PROJECT_ROOT/data/processed"

INPUT_FILE="$RAW_DIR/access.log"
OUTPUT_FILE="$PROCESSED_DIR/extracted_logs.csv"

mkdir -p "$PROCESSED_DIR"

echo "[EXTRACT] Extracting fields from log..."

LC_ALL=C awk '
NF >= 10 &&
$4 ~ /^\[/ &&
$5 ~ /\]$/ &&
$6 ~ /^"/ &&
$9 ~ /^[0-9]{3}$/ &&
$10 ~ /^[0-9-]+$/ {

    ip=$1
    timestamp=substr($4,2) " " substr($5,1,length($5)-1)
    method=substr($6,2)
    endpoint=$7
    status=$9
    size=($10 == "-" ? 0 : $10)

    print ip "," "\"" timestamp "\"" "," method "," endpoint "," status "," size
    next
}

{
    skipped++
}

END {
    print "[EXTRACT] Skipped records:", skipped > "/dev/stderr"
}
' "$INPUT_FILE" > "$OUTPUT_FILE"
echo "[EXTRACT] Done! Saved to $OUTPUT_FILE"
