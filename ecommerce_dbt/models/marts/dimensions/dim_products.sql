SELECT
    product_id,
    title,
    category,
    brand,
    price,
    stock,
    rating
FROM {{ ref('stg_products') }}