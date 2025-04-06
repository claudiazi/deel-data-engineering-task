with

source as (

 select
    customer_address,
    is_active,
    updated_at,
    updated_by,
    created_at,
    customer_name,
    customer_id,
    created_by
 from {{ source('bronze_layer', 'customers') }}
 {% if is_incremental() -%}
   --just in case the cdc is out of order
    where updated_at >= (select max(updated_at) from {{ this }} ) - interval '10 minutes'
 {%- endif -%}
 qualify row_number() over (partition by customer_id order by updated_at desc, _ab_cdc_lsn desc) = 1

)

select * from source
