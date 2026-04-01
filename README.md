# ETL Log Pipeline

## Overview
This project implements an end-to-end ETL (Extract, Transform, Load) pipeline to process web server access logs.

The pipeline ingests raw log data, extracts structured information, transforms it into a clean format, and prepares it for downstream analytics.


## Architecture
Unzip → Extract → Consolidate → Transform → Output CSV

## Features
- Process raw web server log data
- Parse unstructured log format into structured fields
- Data transformation using Bash and Python
- Workflow orchestration using Apache Airflow
- Modular and extensible pipeline design


## Tech Stack
- Python
- Shell scripting
- Apache Airflow
- PostgreSQL ()

## Data Processing

Extract
	•	Parse raw log file into structured columns:
	•	IP address
	•	Timestamp
	•	HTTP method
	•	Endpoint
	•	Status code
	•	Response size

Transform
	•	Clean and standardize data
	•	Convert fields into consistent formats

Load (Next Phase)
	•	Store processed data into PostgreSQL
