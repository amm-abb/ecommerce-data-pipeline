SELECT
    DATE_TRUNC('month', order_date) AS month,
    SUM(revenue) AS revenue,
    SUM(quantity) AS units_sold,
    COUNT(DISTINCT order_id) AS orders
FROM {{ ref('stg_sales') }}
WHERE status = 'completed'
GROUP BY 1
ORDER BY 1