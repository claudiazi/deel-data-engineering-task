 select
    customer_id,
    customer_address,
    is_active as customer_is_active,
    updated_at as customer_updated_at,
    updated_by as customer_updated_by,
    created_at as customer_created_at,
    customer_name,
    created_by as customer_created_by,
from {{ ref('customers') }}