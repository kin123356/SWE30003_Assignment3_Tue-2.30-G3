from models.product import Product

class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add_item(self, product: Product, quantity: int = 1):
        """Add a product to the cart or update its quantity."""
        if product.name in self.items:
            self.items[product.name]['quantity'] += quantity
        else:
            self.items[product.name] = {'product': product.to_dict(), 'quantity': quantity}

    def remove_item(self, product_name: str):
        """Remove a product from the cart."""
        if product_name in self.items:
            del self.items[product_name]

    def update_quantity(self, product_name: str, quantity: int):
        """Update the quantity of a product in the cart."""
        if product_name in self.items:
            if quantity > 0:
                self.items[product_name]['quantity'] = quantity
            else:
                self.remove_item(product_name)

    def get_items(self):
        """Return all items in the cart."""
        return self.items.values()

    def calculate_total(self):
        """Calculate the total price of all items in the cart."""
        total = 0
        for item in self.items.values():
            total += item['product']['price'] * item['quantity']
        return total

    def clear_cart(self):
        """Clear all items from the cart."""
        self.items = {}
