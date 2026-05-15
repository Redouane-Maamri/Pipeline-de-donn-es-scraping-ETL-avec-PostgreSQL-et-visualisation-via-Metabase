from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "owner": "redouane",
    "start_date": datetime(2026, 5, 11),
}

with DAG(
    dag_id="news_pipeline",
    default_args=default_args,
    schedule="@daily",
    catchup=False
) as dag:

    run_pipeline = BashOperator(
        task_id="run_etl_pipeline",
        bash_command="cd /app && python main.py"
    )

    run_pipeline