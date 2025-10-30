import datetime
from models.product import Product
from models.receipt import Receipt

class Order:
    def __init__(self, user_id, items, total, order_id=None, date=None, status="Pending"):
        self.order_id = order_id if order_id else self.generate_order_id()
        self.user_id = user_id
        self.items = items
        self.total = total
        self.date = date if date else datetime.datetime.now()
        self.status = status

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
            'date': self.date.isoformat(),
            'status': self.status
        }

    @staticmethod
    def from_dict(data):
        """Create an Order instance from a dictionary."""
        items = [
            {
                "product": Product.from_dict(item_data["product"]),
                "quantity": item_data["quantity"]
            } 
            for item_data in data["items"]
        ]
        return Order(
            user_id=data['user_id'],
            items=items,
            total=data['total'],
            order_id=data['order_id'],
            date=datetime.datetime.fromisoformat(data['date']),
            status=data['status']
        )
    
    def create_receipt(self):
        return Receipt(self.to_dict())
        
