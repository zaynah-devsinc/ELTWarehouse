SELECT
    id AS customer_id,
    firstName AS first_name,
    lastName AS last_name,
    email,
    gender,
    age,
    phone,

    address.city AS city,
    address.state AS state,
    address.country AS country,

    university,
    role

FROM raw_users