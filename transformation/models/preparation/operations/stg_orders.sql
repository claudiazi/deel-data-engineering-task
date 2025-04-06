 select
    order_id,
    order_date,
    delivery_date,
    updated_at as order_updated_at,
    updated_by as order_updated_by,
    created_at as order_created_at,
    customer_id,
    created_by as order_created_by,
    status as order_status,
    --assume all orders are open if not completed
    case when status = 'COMPLETED' then False
         else True
    end as is_order_open
from {{ ref('orders') }}
