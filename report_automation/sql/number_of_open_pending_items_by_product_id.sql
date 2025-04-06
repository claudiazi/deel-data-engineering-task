select
    product_id,
    product_name,
    count(order_item_id) as number_of_open_pending_items
from marts.main.fct_order_item
where is_order_open = True
group by 1,2