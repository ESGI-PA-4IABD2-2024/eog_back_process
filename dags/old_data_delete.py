from datetime import datetime

from airflow import DAG
from airflow.operators.bash_operator import BashOperator


default_args = {
    "owner": "Antoine",
    "start_date": datetime(2024, 7, 10),
}

with DAG(
    "delete_old_data",
    default_args=default_args,
    schedule_interval="0 3 * * *",
    catchup=False,
) as dag:
    delete_function = BashOperator(
        task_id="delete_function",
        bash_command="cd /opt/airflow/scripts/ && python delete_data.py",
    )
