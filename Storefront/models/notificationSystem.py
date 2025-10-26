class NotificationSystem:
    def send_order_confirmation(self, user_email, order_id):
        """Simulate sending an order confirmation email."""
        print(f"Sending order confirmation for order {order_id} to {user_email}")

    def send_shipment_notification(self, user_email, order_id, tracking_number):
        """Simulate sending a shipment notification email."""
        print(f"Sending shipment notification for order {order_id} to {user_email} with tracking number {tracking_number}")
