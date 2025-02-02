{{
    config(
        materialized='incremental',
        incremental_strategy='merge',
        unique_key=['ds', 'buyer_tax_id']
    )
}}

WITH staging AS (
    SELECT *
    FROM {{ ref('stg_cnpjs') }}
)

SELECT *
FROM staging
