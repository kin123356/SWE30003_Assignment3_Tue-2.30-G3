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
        with open(self.filename, 'r') as f:
            data = json.load(f)
        return data['orders']

    def save_orders(self, orders):
        with open(self.filename, 'w') as f:
            json.dump({"orders": orders}, f, indent=4)

    def place_order(self, order: Order):
        """Save an order to the JSON file."""
        orders = self.load_orders()
        order_dict = order.to_dict()
        # Ensure items are serializable
        order_dict['items'] = [
            {'product': item['product'].to_dict(), 'quantity': item['quantity']}
            for item in order.items
        ]
        orders.append(order_dict)
        self.save_orders(orders)

    def get_order_by_id(self, order_id):
        """Retrieve a single order by its ID."""
        orders = self.load_orders()
        for order_data in orders:
            if order_data['order_id'] == order_id:
                # Reconstruct the Order object
                return Order(
                    user_id=order_data['user_id'],
                    items=order_data['items'],
                    total=order_data['total'],
                    order_id=order_data['order_id'],
                    status=order_data['status']
                )
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
