with cnpjs as (

  select *
  from {{ ref('dim_cnpjs') }}
  where ds = DATE '{{ var("execution_date") }}'

), installments as (

  select *
  from {{ ref('dim_installments') }}
  where ds = DATE '{{ var("execution_date") }}'

), daily_metrics as (

  select
    ds,
    buyer_main_tax_id,
    count(invoice_id) as m_total_invoices,
    count(case when paid_date is not null then invoice_id end) as m_invoices_paid,
    count(case
      when paid_date is null and DATE_DIFF(ds, due_date, DAY) >= 0
        then invoice_id
    end) as m_invoices_open,
    count(case
      when paid_date is null and DATE_DIFF(ds, due_date, DAY) < 28
        then invoice_id
    end) as m_invoices_late_28d,
    sum(original_amount_in_cents) as m_total_original_amount_in_cents,
    sum(expected_amount_in_cents) as m_expected_amount_in_cents,
    sum(paid_amount_in_cents) as m_paid_amount_in_cents,
    sum(case
      when paid_date is not null
        then original_amount_in_cents
      else 0
    end) as m_amount_paid,
    sum(case
      when paid_date is null and DATE_DIFF(ds, due_date, DAY) >= 0
        then original_amount_in_cents
      else 0
    end) as m_amount_open,
    sum(case
      when paid_date is null and DATE_DIFF(ds, due_date, DAY) < 28
        then original_amount_in_cents
      else 0
    end) as m_amount_late_28d

  from installments
  group by 1, 2

)

select
  cnpjs.*,
  coalesce(m_total_invoices, 0) as m_total_invoices,
  coalesce(m_invoices_paid, 0) as m_invoices_paid,
  coalesce(m_invoices_open, 0) as m_invoices_open,
  coalesce(m_invoices_late_28d, 0) as m_invoices_late_28d,
  coalesce(m_total_original_amount_in_cents, 0) as m_total_original_amount_in_cents,
  coalesce(m_expected_amount_in_cents, 0) as m_expected_amount_in_cents,
  coalesce(m_paid_amount_in_cents, 0) as m_paid_amount_in_cents,
  coalesce(m_amount_paid, 0) as m_amount_paid,
  coalesce(m_amount_open, 0) as m_amount_open,
  coalesce(m_amount_late_28d, 0) as m_amount_late_28d
from cnpjs
left join daily_metrics
  on cnpjs.ds = daily_metrics.ds
  and cnpjs.buyer_tax_id = daily_metrics.buyer_main_tax_id
