from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.google.cloud.transfers.postgres_to_gcs import PostgresToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from datetime import datetime

GCP_PROJECT_ID = "temp-task-rafel-rosa"
GCS_BUCKET = "us-central1-test-71c73713data-bucket"

default_args = {
    "owner": "data_engineer",
    "start_date": datetime(2025, 2, 1),
    "retries": 2,
}

with DAG(
    "postgres_to_bigquery",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
) as dag:
    

    extract_cnpjs = DummyOperator(task_id='extract_cnpjs')

    load_cnpjs_bq = DummyOperator(task_id='load_cnpjs_bq')

    extract_installments = DummyOperator(task_id='extract_installments')

    load_installments_bq = DummyOperator(task_id='load_installments_bq')
    
    # extract_companies = PostgresToGCSOperator(
    #     task_id="extract_cnpjs",
    #     postgres_conn_id="postgres_source",
    #     sql="SELECT *, '{{ ds }}'::DATE as ds FROM cnpjs;",
    #     bucket=GCS_BUCKET,
    #     filename="raw/cnpjs/{{ ds }}.parquet",
    #     export_format="parquet",
    # )
# 
    # load_companies_bq = GCSToBigQueryOperator(
    #     task_id="load_cnpjs_bq",
    #     bucket=GCS_BUCKET,
    #     source_objects=["raw/cnpjs/{{ ds }}.parquet"],
    #     destination_project_dataset_table=f"{GCP_PROJECT_ID}.staging.cnpjs",
    #     write_disposition="WRITE_APPEND",
    #     source_format="PARQUET",
    #     time_partitioning={"type": "DAY", "field": "ds"},
    # )
# 
    # extract_installments = PostgresToGCSOperator(
    #     task_id="extract_installments",
    #     postgres_conn_id="postgres_source",
    #     sql="SELECT *, '{{ ds }}'::DATE as ds FROM installments;",
    #     bucket=GCS_BUCKET,
    #     filename="raw/cnpjs/{{ ds }}.parquet",
    #     export_format="parquet",
    # )
# 
    # load_installments_bq = GCSToBigQueryOperator(
    #     task_id="load_installments_bq",
    #     bucket=GCS_BUCKET,
    #     source_objects=["raw/installments/{{ ds }}.parquet"],
    #     destination_project_dataset_table=f"{GCP_PROJECT_ID}.staging.companies",
    #     write_disposition="WRITE_APPEND",
    #     source_format="PARQUET",
    #     time_partitioning={"type": "DAY", "field": "ds"},
    # )
 
    extract_cnpjs >> load_cnpjs_bq
    extract_installments >> load_installments_bq
