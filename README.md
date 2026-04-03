# ETL Log Pipeline

## Overview
This project implements an end-to-end ETL (Extract, Transform, Load) pipeline to process web server access logs (~1.8M records).

The pipeline ingests raw log data, parses unstructured text into structured format, performs data cleaning and transformation, and loads the results into PostgreSQL for downstream analytics.

It supports both **cron-based scheduling** and **Apache Airflow orchestration**, and is designed with a modular, production-style architecture.

---

## Architecture
```
Raw Log (.gz)
↓
Download & Unzip (Bash)
↓
Extract (AWK / Bash)
↓
Transform (Python)
↓
Load (PostgreSQL COPY + Upsert)
```


---

## Features

- End-to-end ETL pipeline for large-scale log processing
- Parses unstructured log data into structured schema
- Handles malformed and invalid records safely
- Bulk loading using PostgreSQL `COPY` for high performance
- Idempotent pipeline design using staging + upsert
- Prevents duplicate records with composite unique constraint
- Supports both cron and Airflow orchestration
- Modular and extensible pipeline structure

---

## Tech Stack

- Python
- Bash / Shell scripting
- PostgreSQL
- Apache Airflow
- Cron (Unix scheduler)

---

## Data Processing

### Extract
- Parses raw log file into structured fields:
  - IP address
  - Timestamp
  - HTTP method
  - Endpoint
  - Status code
  - Response size

### Transform
- Cleans and standardizes extracted data
- Handles encoding issues and malformed rows
- Skips invalid records safely with logging

### Load
- Uses PostgreSQL `COPY` for fast bulk loading
- Loads data into staging table, then upserts into target table
- Ensures idempotent reruns (no duplicate records)

---

## Orchestration

### Cron
- Scheduled daily execution using cron
- Logs both stdout and stderr for debugging

Example: 0 1 * * * scripts/run_pipeline.sh >> logs/pipeline.log 2>&1

### Apache Airflow
- DAG-based orchestration with task dependencies:
  - download → extract → transform → load
- Supports retries and monitoring via UI

---

## Performance

- Processes ~1.89 million log records
- Bulk load completes in ~8 seconds using PostgreSQL
- Efficient handling of large datasets with minimal memory overhead

---

## Reliability Features

- Idempotent pipeline design (safe to rerun)
- Staging-table based upsert
- Composite unique constraint to prevent duplicates
- Logging for debugging and monitoring
- Graceful handling of malformed data

---

## Project Structure
```
etl-log-pipeline/
├── dags/
├── scripts/
├── sql/
├── config/
├── data/
├── logs/
├── README.md
└── requirements.txt
```


---

## Future Improvements

- Add data validation and quality checks
- Convert timestamp to proper PostgreSQL TIMESTAMP type
- Add indexing for query performance
- Extend pipeline with analytics layer (aggregations)
- Containerize pipeline using Docker
