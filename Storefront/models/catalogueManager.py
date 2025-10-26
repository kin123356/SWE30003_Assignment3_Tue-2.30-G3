import json
from models.product import Product

class CatalogueManager:
    def __init__(self, filename="products.json"):
        self.filename = filename

    #Load products from json
    def load_products(self):
        with open(self.filename, "r") as f:
            data = json.load(f)
        return data["products"]

    #Save products to json
    def save_products(self, products):
        with open(self.filename, "w") as f:
            json.dump({"products": products}, f, indent=4)

    #Add product to json file if it doesnt exist
    def add_product(self, product: Product):
        products = self.load_products()
        if product.name in products:
            return False  # Product already exists
        products[product.name] = product.to_dict()
        self.save_products(products)
        return True

    #Update product stock value
    def update_stock(self, product_name, new_stock):
        products = self.load_products()
        if product_name not in products:
            return False
        products[product_name]["stock"] = new_stock
        self.save_products(products)
        return True

    #Delete product in json file
    def delete_product(self, product_name):
        products = self.load_products()
        if product_name in products:
            del products[product_name]  # Remove the product from the dict
            self.save_products(products)  # Save updated products back to JSON
            return True
        return False 
