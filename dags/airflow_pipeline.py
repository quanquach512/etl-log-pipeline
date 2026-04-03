from datetime import timedelta 
# The DAG object; we'll need this to instantiate a DAG
from airflow.models import DAG
#Operators
from airflow.operators.bash_operator import BashOperator

from airflow.utils.dates import days_ago
from pathlib import Path
import logging
import os

os.environ['NO_PROXY'] = '*'
DAG_FILE = Path(__file__).resolve()
PROJECT_ROOT = DAG_FILE.parents[2]
SCRIPT_DIR = PROJECT_ROOT/"scripts"
#args init
default_args = {
    'owner': 'Quan',
    'start_date': days_ago(1),
    'email':['quan@email.com'],
    'retries': 1,
    'retry_delay':timedelta(minutes=5)
}

#define DAG
dag = DAG(
    'ETL_log_pipeline',
    default_args=default_args,
    description="Airflow ETL Log Pipeline",
    schedule_interval="@daily"
)

#define download task
download_task = BashOperator(
    task_id='download',
    bash_command=f"""
        bash "{SCRIPT_DIR}"/download.sh
    """,
    dag=dag
)

#define extract task
extract_task = BashOperator(
    task_id='extract',
    bash_command=f"""
        bash "{SCRIPT_DIR}"/extract.sh
    """,
    dag=dag
)

transform_task = BashOperator(
    task_id='transform',
    bash_command=f"""
        "{PROJECT_ROOT}/venv/bin/python" "{SCRIPT_DIR}/transform.py"
    """,
    dag=dag
)

load_task = BashOperator(
    task_id='load',
    bash_command=f"""
        "{PROJECT_ROOT}/venv/bin/python" "{SCRIPT_DIR}/load.py"
    """,
    dag=dag
)

download_task >> extract_task >> transform_task >> load_task
