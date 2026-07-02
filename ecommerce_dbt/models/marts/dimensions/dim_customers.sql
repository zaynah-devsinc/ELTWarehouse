SELECT
    customer_id,
    first_name,
    last_name,
    email,
    gender,
    age,
    city,
    state,
    country,
    university,
    role
FROM {{ ref('stg_users') }}