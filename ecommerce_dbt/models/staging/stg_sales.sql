SELECT
    order_id,
    customer_id,
    product_id,
    order_date,
    quantity,
    unit_price,
    status,
    revenue
FROM {{ source('raw', 'sales') }}