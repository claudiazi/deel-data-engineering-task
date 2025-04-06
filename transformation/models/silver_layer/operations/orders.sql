with

source as (

 select
    order_date,
    delivery_date,
    updated_at,
    updated_by,
    created_at,
    customer_id,
    order_id,
    created_by,
    status
 from {{ source('bronze_layer', 'orders') }}
 {% if is_incremental() -%}
  --just in case the cdc is out of order
    where updated_at >= (select max(updated_at) from {{ this }} ) - interval '10 minutes'
 {%- endif -%}
 qualify row_number() over (partition by order_id order by updated_at desc, _ab_cdc_lsn desc) = 1

)

select * from source
