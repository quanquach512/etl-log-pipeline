import csv
from pathlib import Path 

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = PROJECT_ROOT/"data/processed/extracted_logs.csv"
OUTPUT_FILE = PROJECT_ROOT/"data/processed/transfomed_logs.csv"


print("[TRANSFORM] Starting...")
skipped = 0
total_rows = 0
with open(INPUT_FILE,'r', encoding="utf-8", errors="replace") as infile, open(OUTPUT_FILE,'w', newline="") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    writer.writerow(["ip", "timestamp", "method", "endpoint", "status", "size"])
    for row in reader:
        try:
            total_rows += 1
            if len(row) != 6:
                skipped += 1
                continue
            ip = row[0]
            timestamp = row[1]

            method  = row[2]
            endpoint = row[3] 

            status = int(row[-2])
            size = int(row[-1])
            writer.writerow([ip,timestamp,method,endpoint,status,size])
        except Exception as e:
            skipped += 1
            print(f"[WARN] Skipping row: {row}")

print(f"[TRANSFORM] Done. Output: {OUTPUT_FILE}")
print(f"[TRANSFORM] number of skipped rows: {skipped}")
print(f"[TRANSFORM] number of total rows: {total_rows}")