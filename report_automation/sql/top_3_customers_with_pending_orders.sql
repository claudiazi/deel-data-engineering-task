select
    customer_id,
    customer_name,
    count(distinct order_id) as number_of_pending_orders
from marts.main.fct_order_item
where is_order_open = True
group by 1,2
order by 3 desc
limit 3