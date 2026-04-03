import csv
import logging 
from pathlib import Path
import psycopg2
from dotenv import load_dotenv
import os
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
                    
PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = PROJECT_ROOT/"data/processed/transformed_logs.csv"
ENV_FILE = PROJECT_ROOT/"config/.env"

load_dotenv(ENV_FILE)
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

UPSERT_SQL = """
INSERT INTO access_logs (
    ip_address,
    event_time,
    method,
    endpoint,
    status_code,
    response_size
)
SELECT DISTINCT
    ip_address,
    event_time,
    method,
    endpoint,
    status_code,
    response_size
FROM access_logs_staging
ON CONFLICT (ip_address, event_time, method, endpoint, status_code, response_size)
DO UPDATE SET
    updated_at = CURRENT_TIMESTAMP;
"""

TRUNCATE_STAGING_SQL = "TRUNCATE TABLE access_logs_staging;"
COUNT_STAGING_SQL = "SELECT COUNT(*) FROM access_logs_staging;"
COUNT_TARGET_SQL = "SELECT COUNT(*) FROM access_logs;"
COPY_STAGING_SQL = "COPY access_logs_staging(ip_address,event_time,method,endpoint,status_code,response_size) FROM STDIN WITH (FORMAT CSV)"

def main() -> None:
    start = time.time()
    logging.info("[LOAD] Starting staging + upsert...")
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            logging.info("[LOAD] Truncating staging table...")
            cur.execute(TRUNCATE_STAGING_SQL)
            logging.info("[LOAD] Copying CSV into staging table....")
            with open(INPUT_FILE, "r", encoding="utf-8", errors="replace") as infile:
                next(infile) #skip header 
                cur.copy_expert(COPY_STAGING_SQL,infile)
            cur.execute(COUNT_STAGING_SQL)
            staging_count = cur.fetchone()[0]
            logging.info(f"[LOAD] Rows copied to staging: {staging_count}")
            logging.info("[LOAD] Upserting from staging into target table...")
            cur.execute(UPSERT_SQL)

            cur.execute(COUNT_TARGET_SQL)
            target_count = cur.fetchone()[0]
            logging.info(f"[LOAD] Total rows currently in access_logs: {target_count}")

            logging.info("[LOAD] Clearing staging table...")
            cur.execute(TRUNCATE_STAGING_SQL)


        conn.commit()
    end = time.time()
    logging.info(f"[LOAD] Done in {end-start:.2f} seconds")
    conn.close()
if __name__ == "__main__":
    main() 
                

