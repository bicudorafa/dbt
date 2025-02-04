from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.sensors.external_task import ExternalTaskSensor
from datetime import datetime, timedelta


default_args = {
    'owner': 'data_engineer',
    'start_date': datetime(2024, 7, 20),
    'retries': 2,
}

with DAG(
    'dbt_build_dag',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
) as dbt_dag:

    wait_for_extraction = ExternalTaskSensor(
        task_id='wait_for_extraction',
        external_dag_id='postgres_to_bigquery_incremental',
        external_task_id='end_extraction',
        allowed_states=['success'],
        failed_states=['failed', 'skipped'],
        execution_delta=timedelta(hours=1),
        mode='reschedule',
        poke_interval=300,
        timeout=3600,
    )

    bronze_intermediary = BashOperator(
        task_id='bronze_intermediary',
        bash_command=(
            'dbt build -s "tag:intermediary,models/bronze/" --vars \'{"execution_date": "{{ ds }}"}\''
        ),
    )

    silver_incremental = BashOperator(
        task_id='silver_incremental',
        bash_command=(
            'dbt build -s "tag:incremental,models/silver/" --vars \'{"execution_date": "{{ ds }}"}\''
        ),
    )

    gold_intermediary = BashOperator(
        task_id='gold_intermediary',
        bash_command=(
            'dbt build -s "tag:incremental,models/silver/" --vars \'{"execution_date": "{{ ds }}"}\''
        ),
    )

    gold_incremental = BashOperator(
        task_id='gold_incremental',
        bash_command=(
            'dbt build -s "tag:incremental,models/silver/" --vars \'{"execution_date": "{{ ds }}"}\''
        ),
    )

    generate_docs = BashOperator(
        task_id='generate_docs',
        bash_command='dbt docs generate --vars \'{"execution_date": "{{ ds }}"}\'',
    )

    (
        wait_for_extraction >> bronze_intermediary >> silver_incremental >> 
        gold_intermediary >> gold_incremental >> generate_docs
    )
