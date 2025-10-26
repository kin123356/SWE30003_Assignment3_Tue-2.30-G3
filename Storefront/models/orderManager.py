import json
import os
from models.order import Order

class OrderManager:
    def __init__(self, filename="orders.json"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                json.dump({"orders": []}, f)

    def load_orders(self):
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, 'r') as f:
            data = json.load(f)
            # Use the from_dict method to reconstruct Order objects
            return [Order.from_dict(order_data) for order_data in data.get('orders', [])]

    def save_orders(self, orders):
        with open(self.filename, 'w') as f:
            json.dump({"orders": [order.to_dict() for order in orders]}, f, indent=4)

    def place_order(self, order: Order):
        """Save an order to the JSON file."""
        orders = self.load_orders()
        orders.append(order)
        self.save_orders(orders)

    def get_order_by_id(self, order_id):
        """Retrieve a single order by its ID."""
        orders = self.load_orders()
        for order_data in orders:
            if order_data.order_id == order_id:
                return order_data
        return None

    def update_order_status(self, order_id, status):
        """Update the status of a specific order."""
        with open(self.filename, 'r+') as f:
            data = json.load(f)
            for order in data['orders']:
                if order['order_id'] == order_id:
                    order['status'] = status
                    break
            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4)

    def get_orders_for_user(self, user_id):
        """Retrieve all orders for a specific user."""
        with open(self.filename, 'r') as f:
            data = json.load(f)
        return [order for order in data['orders'] if order['user_id'] == user_id]
