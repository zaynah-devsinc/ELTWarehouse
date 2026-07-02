SELECT
    id AS cart_id,
    userId AS customer_id,
    total,
    discountedTotal AS discounted_total,
    totalProducts AS total_products,
    totalQuantity AS total_quantity,
    products
FROM raw_carts