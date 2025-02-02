with current_partition as (

    select *
    from `temp-task-rafel-rosa.staging.raw_installments`
    where ds = DATE '{{ var("execution_date") }}'

)

select
    ds,
    asset_id,
    invoice_id,
    buyer_tax_id,
    original_amount_in_cents,
    expected_amount_in_cents,
    paid_amount_in_cents,
    buyer_main_tax_id AS buyer_main_tax_id,
    PARSE_DATE('%Y-%m-%d', invoice_issue_date) AS invoice_issue_date,
    PARSE_DATE('%Y-%m-%d', due_date) AS due_date,
    parse_date('%Y-%m-%d',nullif(paid_date, "None")) AS paid_date,
from current_partition
