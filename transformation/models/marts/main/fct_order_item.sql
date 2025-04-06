{{ config(
    materialized = 'incremental',
    unique_key = 'order_item_id',
    cluster_by = ['order_item_updated_at']
) }}

with source_data as (
    select
        oi.order_item_id,
        oi.product_id,
        oi.order_id,
        oi.order_item_updated_at,
        o.delivery_date,
        o.order_status,
        o.is_order_open,
        p.product_name,
        o.customer_id,
        c.customer_name
    from {{ ref('stg_order_items') }} oi
    inner join {{ ref('stg_orders') }} o
        on oi.order_id = o.order_id
    inner join {{ ref('stg_products') }} p
        on oi.product_id = p.product_id
    inner join {{ ref('stg_customers') }} c
        on o.customer_id = c.customer_id
    {% if is_incremental() %}
        where oi.order_item_updated_at > (
            select max(order_item_updated_at) - interval '10 minutes' from {{ this }}
        ) --just in case the cdc is out of order
    {% endif %}
)

select *
from source_data
