{{
    config(
        materialized='incremental',
        incremental_strategy='merge',
        unique_key=['ds', 'buyer_tax_id']
    )
}}

with daily_metrics as (

    select * from {{ ref('int_daily_cnpj_metrics') }}

)

select *
from daily_metrics