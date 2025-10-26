class Payment:
    def __init__(self, order_id, amount):
        self.payment_id = f"pay_{order_id}"
        self.order_id = order_id
        self.amount = amount
        self.status = "Pending"

    def process_payment(self):
        """Simulate processing the payment."""
        self.status = "Completed"
        return True

    def to_dict(self):
        return {
            'payment_id': self.payment_id,
            'order_id': self.order_id,
            'amount': self.amount,
            'status': self.status
        }
