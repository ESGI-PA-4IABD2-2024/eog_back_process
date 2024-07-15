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
    "alimentation_metros",
    default_args=default_args,
    schedule_interval="*/15 3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,00 * * *",
    catchup=False,
) as dag:
    metro_1 = BashOperator(
        task_id="metro_1",
        bash_command="cd /opt/airflow/scripts/ && python prim_api_usage.py -ligne Metro_1",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    metro_2 = BashOperator(
        task_id="metro_2",
        bash_command="cd /opt/airflow/scripts/ && python prim_api_usage.py -ligne Metro_2",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    metro_3 = BashOperator(
        task_id="metro_3",
        bash_command="cd /opt/airflow/scripts/ && python prim_api_usage.py -ligne Metro_3",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    metro_3B = BashOperator(
        task_id="metro_3B",
        bash_command="cd /opt/airflow/scripts/ && python prim_api_usage.py -ligne Metro_3B",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    metro_4 = BashOperator(
        task_id="metro_4",
        bash_command="cd /opt/airflow/scripts/ && python prim_api_usage.py -ligne Metro_4",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    metro_5 = BashOperator(
        task_id="metro_5",
        bash_command="cd /opt/airflow/scripts/ && python prim_api_usage.py -ligne Metro_5",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    metro_6 = BashOperator(
        task_id="metro_6",
        bash_command="cd /opt/airflow/scripts/ && python prim_api_usage.py -ligne Metro_6",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    metro_7 = BashOperator(
        task_id="metro_7",
        bash_command="cd /opt/airflow/scripts/ && python prim_api_usage.py -ligne Metro_7",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    metro_7B = BashOperator(
        task_id="metro_7B",
        bash_command="cd /opt/airflow/scripts/ && python prim_api_usage.py -ligne Metro_7B",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    metro_8 = BashOperator(
        task_id="metro_8",
        bash_command="cd /opt/airflow/scripts/ && python prim_api_usage.py -ligne Metro_8",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    metro_9 = BashOperator(
        task_id="metro_9",
        bash_command="cd /opt/airflow/scripts/ && python prim_api_usage.py -ligne Metro_9",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    metro_10 = BashOperator(
        task_id="metro_10",
        bash_command="cd /opt/airflow/scripts/ && python prim_api_usage.py -ligne Metro_10",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    metro_11 = BashOperator(
        task_id="metro_11",
        bash_command="cd /opt/airflow/scripts/ && python prim_api_usage.py -ligne Metro_11",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    metro_12 = BashOperator(
        task_id="metro_12",
        bash_command="cd /opt/airflow/scripts/ && python prim_api_usage.py -ligne Metro_12",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    metro_13 = BashOperator(
        task_id="metro_13",
        bash_command="cd /opt/airflow/scripts/ && python prim_api_usage.py -ligne Metro_13",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    metro_14 = BashOperator(
        task_id="metro_14",
        bash_command="cd /opt/airflow/scripts/ && python prim_api_usage.py -ligne Metro_14",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    orlyval = BashOperator(
        task_id="orlyval",
        bash_command="cd /opt/airflow/scripts/ && python prim_api_usage.py -ligne Orlyval",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    chain(
        metro_1,
        metro_2,
        metro_3,
        metro_3B,
        metro_4,
        metro_5,
        metro_6,
        metro_7,
        metro_7B,
        metro_8,
        metro_9,
        metro_10,
        metro_11,
        metro_12,
        metro_13,
        metro_14,
        orlyval,
    )
