{{ config(tags = ['intermediary']) }}

with current_partition as (

    select *
    from `temp-task-rafel-rosa.staging.raw_cnpjs`
    where ds = DATE '{{ var("execution_date") }}'

)

select
    ds,
    buyer_tax_id,
    share_capital,
    company_size,
    legal_nature,
    simples_option,
    is_mei,
    is_main_company,
    company_status,
    is_active,
    zipcode,
    main_cnae,
    state,
    uf,
    city,
    created_at,
    updated_at
from current_partition
