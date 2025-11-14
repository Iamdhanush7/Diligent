-- report.sql
SELECT
  u.user_id,
  u.name AS user_name,
  u.email,
  o.order_id,
  o.order_date,
  p.product_id,
  p.name AS product_name,
  oi.quantity,
  oi.price_each,
  (oi.quantity * oi.price_each) AS item_total
FROM orders o
JOIN users u ON o.user_id = u.user_id
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p ON p.product_id = oi.product_id
ORDER BY o.order_date DESC
LIMIT 200;
