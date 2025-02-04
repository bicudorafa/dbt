# DBT / Composer Sample Project

This is a sample project of how to design a DBT project and run it on Google Cloud Composer (GCP's Serverless Airflow). The full description of the project design is [here](https://docs.google.com/document/d/1qhsTLGgzjPeXni7a8GlFjYAF7Bdqw46wru5Q-XqJK24/edit?tab=t.0)

## Setup

To setup your environment, you need ```uv``` as your Python manager. After it, just run:
```
uv install
```
After creating your environemnt, you need to authenticate your connection to GCP. The steps necessary for doing so are in this [Medium Article](https://medium.com/@yuliia.tkachova/how-to-run-dbt-airflow-on-google-cloud-0e216a9bc420)

## Contents
There are 2 main sections in this project:
- dags: folder containing the DAGs to be used at Cloud Composer
- temp_rafael_rosa: the dbt project used to make Data Transformations at BigQuery
