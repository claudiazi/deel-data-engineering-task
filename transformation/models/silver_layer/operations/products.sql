with

source as (

 select
    unity_price,
    is_active,
    updated_at,
    product_id,
    updated_by,
    created_at,
    product_name,
    barcode,
    created_by
 from {{ source('bronze_layer', 'products') }}
 {% if is_incremental() -%}
  --just in case the cdc is out of order
    where updated_at >= (select max(updated_at) from {{ this }} ) - interval '10 minutes'
 {%- endif -%}
 qualify row_number() over (partition by product_id order by updated_at desc, _ab_cdc_lsn desc) = 1

)

select * from source
