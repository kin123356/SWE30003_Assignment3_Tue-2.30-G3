import datetime

class Order:
    def __init__(self, user_id, items, total):
        self.order_id = self.generate_order_id()
        self.user_id = user_id
        self.items = items
        self.total = total
        self.order_date = datetime.datetime.now()
        self.status = "Pending"

    def update_status(self, status):
        self.status = status

    def generate_order_id(self):
        """Generate a unique order ID."""
        return str(int(datetime.datetime.now().timestamp()))

    def to_dict(self):
        """Return a dictionary representation of the order."""
        return {
            'order_id': self.order_id,
            'user_id': self.user_id,
            'items': [{"product": item['product'].to_dict(), "quantity": item['quantity']} for item in self.items],
            'total': self.total,
            'date': self.order_date.isoformat(),  # Convert datetime to string
            'status': self.status
        }
