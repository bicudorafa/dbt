auth-gcloud:
	gcloud auth application-default login

run-backfill-composer:
	gcloud composer environments run test \
    	--location us-central1 \
        dags trigger -- dbt_transformation_dag --exec-date 2024-07-20T00:00:01

run-bronze-intermediary:
	dbt run --select "tag:intermediary,models/bronze/" --vars '{"execution_date": "2024-07-20"}'

test-bronze-intermediary:
	dbt test --select "tag:intermediary,models/bronze/" --vars '{"execution_date": "2024-07-20"}'

run-bronze-incremental:
	dbt run --select "tag:incremental,models/bronze/" --vars '{"execution_date": "2024-07-20"}'

test-bronze-incremental:
	dbt test --select "tag:incremental,models/bronze/" --vars '{"execution_date": "2024-07-20"}'

run-silver-intermediary:
	dbt run --select "tag:intermediary,models/silver/" --vars '{"execution_date": "2024-07-20"}'

test-silver-intermediary:
	dbt test --select "tag:intermediary,models/silver/" --vars '{"execution_date": "2024-07-20"}'

run-silver-incremental:
	dbt run --select "tag:incremental,models/silver/" --vars '{"execution_date": "2024-07-20"}'

test-silver-incremental:
	dbt test --select "tag:incremental,models/silver/" --vars '{"execution_date": "2024-07-20"}'

run-gold-intermediary:
	dbt run --select "tag:intermediary,models/gold/" --vars '{"execution_date": "2024-07-20"}'

test-gold-intermediary:
	dbt test --select "tag:intermediary,models/gold/" --vars '{"execution_date": "2024-07-20"}'

run-gold-incremental:
	dbt run --select "tag:incremental,models/gold/" --vars '{"execution_date": "2024-07-20"}'

test-gold-incremental:
	dbt test --select "tag:incremental,models/gold/" --vars '{"execution_date": "2024-07-20"}'