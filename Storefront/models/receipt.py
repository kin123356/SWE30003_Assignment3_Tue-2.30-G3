class Receipt:
    def __init__(self, order):
        self.order_id = order["order_id"]
        self.date = order["date"]
        self.user_id = order["user_id"]
        self.items = order["items"]
        self.total = order["total"]

    def display(self):
        return (
            f"Order #{self.order_id}\n"
            f"Date: {self.date}\n"
            f"User ID: {self.user_id}\n"
            f"Items: {len(self.items)}\n"
            f"Total: ${self.total:.2f}\n"
        )
