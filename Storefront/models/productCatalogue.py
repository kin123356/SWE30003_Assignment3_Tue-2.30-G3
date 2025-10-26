import json
import os
from models.product import Product

class ProductCatalogue:
    def __init__(self, filename="products.json"):
            self.filename = filename
            if not os.path.exists(filename):
                self._create_default_catalogue()

    #Create default products so always something to display
    def _create_default_catalogue(self):
        default_products = {
            "products": {
                "1": Product("Bread", "A Loaf of Bread", 3.00, 6).to_dict(),
                "2": Product("Milk", "1L Carton of Milk", 2.00, 4).to_dict(),
                "3": Product("Eggs", "A Carton of Eggs", 7.00, 9).to_dict(),
                "4": Product("Water", "A Bottle of Water", 1.50, 12).to_dict()
            }
        }
        with open(self.filename, "w") as f:
            json.dump(default_products, f, indent=4)

    #Read products from json
    def load_products(self):
        with open(self.filename, "r") as f:
            data = json.load(f)
        return {k: Product.from_dict(v) for k, v in data["products"].items()}

    def get_all_products(self):
        """Retrieve all products from the catalogue."""
        return self.load_products()

    def get_product(self, product_name: str) -> Product | None:
        """Retrieve a single product by its name."""
        products = self.load_products()
        for product in products.values():
            if product.name == product_name:
                return product
        return None

    def delete_product(self, product_name):
        products = self.load_products()
        products = {k: v for k, v in products.items() if v.name != product_name}
        self.save_products(products)
        return True

    def update_product_details(self, product_name, price, stock, is_available):
        products = self.load_products()
        for product in products.values():
            if product.name == product_name:
                product.price = price
                product.stock = stock
                product.is_available = is_available
                break
        self.save_products(products)


    def save_products(self, products):
        data = {"products": {k: v.to_dict() for k, v in products.items()}}
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)