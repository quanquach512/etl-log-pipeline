import csv
import logging 
from pathlib import Path
import psycopg2
from dotenv import load_dotenv
import os
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
                    
PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = PROJECT_ROOT/"data/processed/transfomed_logs.csv"
ENV_FILE = PROJECT_ROOT/"config/.env"

load_dotenv(ENV_FILE)
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

def main() -> None:
    start = time.time()
    logging.info("[LOAD] Starting loading step...")
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            with open(INPUT_FILE, "r", encoding="utf-8", errors="replace") as infile:
                next(infile)
                cur.copy_expert(
                    """
                    COPY access_logs(ip_address,event_time,method,endpoint,status_code,response_size)
                    FROM STDIN WITH (FORMAT CSV)
                    """,
                    infile,
                )
        conn.commit()
        end = time.time()
    logging.info(f"[LOAD] Done in {end-start:.2f} seconds")
    conn.close()
if __name__ == "__main__":
    main() 
                

