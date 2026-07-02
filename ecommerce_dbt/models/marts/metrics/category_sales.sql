SELECT
    p.category,

    SUM(f.quantity) AS units_sold,

    SUM(f.discounted_total) AS revenue

FROM {{ ref('fact_order_items') }} f

JOIN {{ ref('dim_products') }} p
ON f.product_id = p.product_id

GROUP BY p.category

ORDER BY revenue DESC