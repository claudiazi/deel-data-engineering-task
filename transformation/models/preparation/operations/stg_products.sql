select
    product_id,
    unity_price as product_price,
    is_active as product_is_active,
    updated_at as product_updated_at,
    updated_by as product_updated_by,
    created_at as product_created_at,
    product_name,
    barcode as product_barcode,
    created_by as product_created_by
from {{ ref('products') }}
