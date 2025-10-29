import json
from models.product import Product

class CatalogueManager:
    def __init__(self, filename="products.json"):
        self.filename = filename

    #Load products from json
    def load_products(self):
        with open(self.filename, "r") as f:
            data = json.load(f)
        return {k: Product.from_dict(v) for k, v in data["products"].items()}

    #Add product to json file if it doesnt exist
    def add_product(self, product: Product):
        products = self.load_products()
        #Stop duplicate products from being added, Checks product names in JSON file
        if any(p.name == product.name for p in products.values()):
            return False
        new_id = str(len(products) + 1)
        products[new_id] = product
        self.save_products(products)
        return True

    #Delete products from JSON file
    def delete_product(self, product_name):
        products = self.load_products()
        products = {k: v for k, v in products.items() if v.name != product_name}
        self.save_products(products)
        return True

    #Update the infomation of a Product in JSON
    def update_product_details(self, product_name, price, stock, is_available):
        products = self.load_products()
        for product in products.values():
            if product.name == product_name:
                product.price = price
                product.stock = stock
                product.is_available = is_available
                break
        self.save_products(products)

    #Save new product to JSON file (Commits the change)
    def save_products(self, products):
        data = {"products": {k: v.to_dict() for k, v in products.items()}}
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)