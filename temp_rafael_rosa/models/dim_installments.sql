{{
    config(
        materialized='incremental',
        incremental_strategy='merge',
        unique_key=['ds', 'invoice_id']
    )
}}

WITH staging AS (
    SELECT *
    FROM {{ ref('stg_installments') }}
)

SELECT *
FROM staging
