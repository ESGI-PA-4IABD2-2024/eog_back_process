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
    "alimentation_rer_transiliens",
    default_args=default_args,
    schedule_interval="0 1 * * *",
    catchup=False,
) as dag:
    rer_A = BashOperator(
        task_id="rer_A",
        bash_command="cd /opt/airflow/scripts/ && python navitia_api_usage.py -ligne A",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    rer_B = BashOperator(
        task_id="rer_B",
        bash_command="cd /opt/airflow/scripts/ && python navitia_api_usage.py -ligne B",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    rer_C = BashOperator(
        task_id="rer_C",
        bash_command="cd /opt/airflow/scripts/ && python navitia_api_usage.py -ligne C",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    rer_D = BashOperator(
        task_id="rer_D",
        bash_command="cd /opt/airflow/scripts/ && python navitia_api_usage.py -ligne D",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    rer_E = BashOperator(
        task_id="rer_E",
        bash_command="cd /opt/airflow/scripts/ && python navitia_api_usage.py -ligne E",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    transilien_H = BashOperator(
        task_id="transilien_H",
        bash_command="cd /opt/airflow/scripts/ && python navitia_api_usage.py -ligne H",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    transilien_J = BashOperator(
        task_id="transilien_J",
        bash_command="cd /opt/airflow/scripts/ && python navitia_api_usage.py -ligne J",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    transilien_K = BashOperator(
        task_id="transilien_K",
        bash_command="cd /opt/airflow/scripts/ && python navitia_api_usage.py -ligne K",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    transilien_L = BashOperator(
        task_id="transilien_L",
        bash_command="cd /opt/airflow/scripts/ && python navitia_api_usage.py -ligne L",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    transilien_N = BashOperator(
        task_id="transilien_N",
        bash_command="cd /opt/airflow/scripts/ && python navitia_api_usage.py -ligne N",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    transilien_P = BashOperator(
        task_id="transilien_P",
        bash_command="cd /opt/airflow/scripts/ && python navitia_api_usage.py -ligne P",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    transilien_R = BashOperator(
        task_id="transilien_R",
        bash_command="cd /opt/airflow/scripts/ && python navitia_api_usage.py -ligne R",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    transilien_U = BashOperator(
        task_id="transilien_U",
        bash_command="cd /opt/airflow/scripts/ && python navitia_api_usage.py -ligne U",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    transilien_V = BashOperator(
        task_id="transilien_V",
        bash_command="cd /opt/airflow/scripts/ && python navitia_api_usage.py -ligne V",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    chain(
        rer_A,
        rer_B,
        rer_C,
        rer_D,
        rer_E,
        transilien_H,
        transilien_J,
        transilien_K,
        transilien_L,
        transilien_N,
        transilien_P,
        transilien_R,
        transilien_U,
        transilien_V,
    )
