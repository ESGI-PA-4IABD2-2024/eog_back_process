from datetime import datetime

from airflow import DAG
from airflow.models.baseoperator import chain
from airflow.operators.bash_operator import BashOperator
from airflow.utils.trigger_rule import TriggerRule

default_args = {
    "owner": "Antoine",
    "start_date": datetime(2024, 7, 6),
}

with DAG(
    "alimentation_tramways",
    default_args=default_args,
    schedule_interval="*/15 5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,00,1,2 * * *",
    catchup=False,
) as dag:
    tramway_1 = BashOperator(
        task_id="tramway_1",
        bash_command="cd /opt/airflow/scripts/ && python prim_api_usage.py -ligne Tram_1",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    tramway_2 = BashOperator(
        task_id="tramway_2",
        bash_command="cd /opt/airflow/scripts/ && python prim_api_usage.py -ligne Tram_2",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    tramway_3A = BashOperator(
        task_id="tramway_3A",
        bash_command="cd /opt/airflow/scripts/ && python prim_api_usage.py -ligne Tram_3A",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    tramway_3B = BashOperator(
        task_id="tramway_3B",
        bash_command="cd /opt/airflow/scripts/ && python prim_api_usage.py -ligne Tram_3B",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    tramway_4 = BashOperator(
        task_id="tramway_4",
        bash_command="cd /opt/airflow/scripts/ && python prim_api_usage.py -ligne Tram_4",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    tramway_5 = BashOperator(
        task_id="tramway_5",
        bash_command="cd /opt/airflow/scripts/ && python prim_api_usage.py -ligne Tram_5",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    tramway_6 = BashOperator(
        task_id="tramway_6",
        bash_command="cd /opt/airflow/scripts/ && python prim_api_usage.py -ligne Tram_6",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    tramway_7 = BashOperator(
        task_id="tramway_7",
        bash_command="cd /opt/airflow/scripts/ && python prim_api_usage.py -ligne Tram_7",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    tramway_8 = BashOperator(
        task_id="tramway_8",
        bash_command="cd /opt/airflow/scripts/ && python prim_api_usage.py -ligne Tram_8",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    tramway_9 = BashOperator(
        task_id="tramway_9",
        bash_command="cd /opt/airflow/scripts/ && python prim_api_usage.py -ligne Tram_9",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    tramway_10 = BashOperator(
        task_id="tramway_10",
        bash_command="cd /opt/airflow/scripts/ && python prim_api_usage.py -ligne Tram_10",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    tramway_11 = BashOperator(
        task_id="tramway_11",
        bash_command="cd /opt/airflow/scripts/ && python prim_api_usage.py -ligne Tram_11",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    tramway_12 = BashOperator(
        task_id="tramway_12",
        bash_command="cd /opt/airflow/scripts/ && python prim_api_usage.py -ligne Tram_12",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    tramway_13 = BashOperator(
        task_id="tramway_13",
        bash_command="cd /opt/airflow/scripts/ && python prim_api_usage.py -ligne Tram_13",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    chain(
        tramway_1,
        tramway_2,
        tramway_3A,
        tramway_3B,
        tramway_4,
        tramway_5,
        tramway_6,
        tramway_7,
        tramway_8,
        tramway_9,
        tramway_10,
        tramway_11,
        tramway_12,
        tramway_13,
    )
