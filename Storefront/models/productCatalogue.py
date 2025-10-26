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
        return data["products"]
        