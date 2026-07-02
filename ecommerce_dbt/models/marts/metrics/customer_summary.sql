SELECT

    c.customer_id,

    c.first_name,

    c.last_name,

    COUNT(f.cart_id) AS total_orders,

    SUM(f.total) AS lifetime_value,

    AVG(f.total) AS average_order_value

FROM {{ ref('fact_orders') }} f

JOIN {{ ref('dim_customers') }} c

ON f.customer_id = c.customer_id

GROUP BY

    c.customer_id,

    c.first_name,

    c.last_name

ORDER BY lifetime_value DESC