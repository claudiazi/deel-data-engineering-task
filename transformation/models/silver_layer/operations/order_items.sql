with

source as (

 select
     order_item_id,
     product_id,
     order_id,
     quanity,
     created_at,
     created_by,
     updated_at,
     updated_by
 from {{ source('bronze_layer', 'order_items') }}
 {% if is_incremental() -%}
   --just in case the cdc is out of order
    where updated_at >= (select max(updated_at) from {{ this }} ) - interval '10 minutes'
 {%- endif -%}
 qualify row_number() over (partition by order_item_id order by updated_at desc, _ab_cdc_lsn desc) = 1

)

select * from source
