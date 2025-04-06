select
    delivery_date,
    order_status,
    count(order_id) as number_of_open_orders
from preparation.operations.stg_orders
where is_order_open = True
group by 1,2