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
    'dbt_transformation_dag',
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

    run_dbt = BashOperator(
        task_id='run_dbt',
        bash_command=(
            'ls -lah /home/airflow/gcs/dags/temp_rafael_rosa/ && '
            'cd /home/airflow/gcs/dags/temp_rafael_rosa/ && '
            'dbt run --profiles-dir . --vars \'{"execution_date": "{{ ds }}"}\''
        ),
    )

    wait_for_extraction >> run_dbt