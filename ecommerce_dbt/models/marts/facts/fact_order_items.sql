SELECT
    c.cart_id,
    c.customer_id,

    p.id AS product_id,
    p.title AS product_title,
    p.price,
    p.quantity,
    p.total,
    p.discountPercentage AS discount_percentage,
    p.discountedTotal AS discounted_total

FROM {{ ref('stg_carts') }} AS c,
UNNEST(c.products) AS t(p)