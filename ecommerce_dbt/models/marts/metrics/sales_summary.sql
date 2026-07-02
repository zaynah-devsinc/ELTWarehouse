SELECT
    COUNT(*) AS total_orders,
    SUM(total) AS total_revenue,
    AVG(total) AS average_order_value,
    SUM(total_quantity) AS total_items_sold
FROM {{ ref('fact_orders') }}