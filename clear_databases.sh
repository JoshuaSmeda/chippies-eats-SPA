order_db="order.db"
echo "Purging ${order_db}"
sqlite3 $order_db << EOF
DELETE FROM Orders;
VACUUM;
EOF
