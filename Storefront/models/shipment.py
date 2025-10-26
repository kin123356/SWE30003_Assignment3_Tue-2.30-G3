class Shipment:
    def __init__(self, order_id, address):
        self.shipment_id = f"shp_{order_id}"
        self.order_id = order_id
        self.address = address
        self.status = "Pending"

    def create_shipment(self):
        """Simulate creating a shipment."""
        self.status = "Shipped"
        return True

    def to_dict(self):
        return {
            'shipment_id': self.shipment_id,
            'order_id': self.order_id,
            'address': self.address,
            'status': self.status
        }
