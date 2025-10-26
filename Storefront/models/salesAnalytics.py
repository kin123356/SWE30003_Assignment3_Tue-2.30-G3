import json
from collections import Counter
from datetime import datetime, timedelta

class SalesAnalytics:
    def __init__(self, orders_filename="orders.json"):
        self.orders_filename = orders_filename

    def _load_orders(self):
        """Load orders from the JSON file."""
        try:
            with open(self.orders_filename, 'r') as f:
                data = json.load(f)
            return data.get('orders', [])
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _get_orders_last_30_days(self):
        """Helper method to retrieve all orders from the last 30 days."""
        try:
            with open(self.orders_filename, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

        orders = data.get('orders', [])
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_orders = []
        for order in orders:
            if 'date' in order:
                try:
                    order_date = datetime.fromisoformat(order['date'])
                    if order_date > thirty_days_ago:
                        recent_orders.append(order)
                except (ValueError, TypeError):
                    continue # Skip orders with invalid date format
        return recent_orders

    def get_total_sales(self):
        """Calculate the total revenue from all completed orders."""
        orders = self._load_orders()
        total_sales = 0
        for order in orders:
            if order['status'] in ['Paid', 'Shipped']:
                total_sales += order['total']
        return total_sales

    def get_total_sales_last_30_days(self):
        recent_orders = self._get_orders_last_30_days()
        return sum(order['total'] for order in recent_orders)

    def get_total_orders_last_30_days(self):
        return len(self._get_orders_last_30_days())

    def get_top_selling_products(self, top_n=5):
        """Find the best-selling products by quantity."""
        orders = self._load_orders()
        product_counts = Counter()
        for order in orders:
            if order['status'] in ['Paid', 'Shipped']:
                for item in order['items']:
                    product_name = item['product']['name']
                    quantity = item['quantity']
                    product_counts[product_name] += quantity
        
        return product_counts.most_common(top_n)
