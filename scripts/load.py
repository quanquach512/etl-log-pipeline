import csv
import logging 
from pathlib import Path
import psycopg2
from dotenv import load_dotenv
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
                    
PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = PROJECT_ROOT/"data/processed/transfomed_logs.csv"
ENV_FILE = PROJECT_ROOT/"config/.env"
BATCH_SIZE = 5000

load_dotenv(ENV_FILE)
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

INSERT_SQL = """
INSERT INTO access_logs (
    ip_address,
    event_time,
    method,
    endpoint,
    status_code,
    response_size
) VALUES (%s, %s, %s, %s, %s, %s)
"""

def main() -> None:
    logging.info("[LOAD] Starting loading step...")
    inserted = 0
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            with open(INPUT_FILE, "r", encoding="utf-8", errors="replace") as infile:
                reader = csv.DictReader(infile)
                batch = []

                for row in reader:
                    batch.append(
                        (
                            row["ip"],
                            row["timestamp"],
                            row["method"],
                            row["endpoint"],
                            int(row["status"]),
                            int(row["size"]),
                        )
                    )

                    if len(batch) >= BATCH_SIZE:
                        cur.executemany(INSERT_SQL, batch)
                        inserted += len(batch)
                        logging.info(f"[LOAD] Inserted {inserted} rows so far....")
                        batch.clear()
                if batch:
                    cur.executemany(INSERT_SQL, batch)
                    inserted += len(batch)
        conn.commit()
    logging.info(f"[LOAD] Done. Inserted rows: {inserted}")

if __name__ == "__main__":
    main() 
                

