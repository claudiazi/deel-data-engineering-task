select 
    order_item_id,
    product_id,
    order_id,
    quanity as order_item_quantity,
    created_at as order_item_created_at,
    created_by as order_item_created_by,
    updated_at as order_item_updated_at,
    updated_by as order_item_updated_by
from {{ ref('order_items') }}
