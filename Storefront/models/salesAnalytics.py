import json
from collections import Counter

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

    def get_total_sales(self):
        """Calculate the total revenue from all completed orders."""
        orders = self._load_orders()
        total_sales = 0
        for order in orders:
            if order['status'] in ['Paid', 'Shipped']:
                total_sales += order['total']
        return total_sales

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
