# Revenue by day
SELECT
    order_date,
    SUM(revenue) AS daily_revenue
FROM sales
WHERE status = 'completed'
GROUP BY order_date
ORDER BY order_date;

# Revenue by week
SELECT
    DATE_TRUNC('week', order_date::timestamp)::date AS week,
    SUM(revenue) AS weekly_revenue
FROM sales
GROUP BY 1
ORDER BY 1;

# Revenue by month
SELECT
    DATE_TRUNC('month', order_date::timestamp)::date AS month,
    SUM(revenue) AS monthly_revenue
FROM sales
GROUP BY 1
ORDER BY 1;

# top product
SELECT
    product_id,
    SUM(quantity) AS units_sold,
    SUM(revenue) AS revenue
FROM sales
WHERE status = 'completed'
GROUP BY product_id
ORDER BY revenue DESC
LIMIT 10;

# customer value
SELECT
    c.name,
    p.product_name,
    SUM(s.revenue) AS customer_value
FROM sales s
LEFT JOIN customers c ON s.customer_id = c.customer_id
LEFT JOIN products p ON s.product_id = p.product_id
GROUP BY c.name, p.product_name 
ORDER BY customer_value DESC;

DROP TABLE customers, products, sales; 


