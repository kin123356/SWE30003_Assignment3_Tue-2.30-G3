import json

class Inventory:
    def __init__(self, filename="products.json"):
        self.filename = filename

    def get_stock(self, product_name):
        """Get the stock level for a specific product."""
        with open(self.filename, 'r') as f:
            data = json.load(f)
        for product_data in data['products'].values():
            if product_data['name'] == product_name:
                return product_data['stock']
        return 0

    def set_stock(self, product_name, new_stock):
        """Set the stock level for a product to a specific value."""
        with open(self.filename, 'r+') as f:
            data = json.load(f)
            for product_id, product_data in data['products'].items():
                if product_data['name'] == product_name:
                    product_data['stock'] = new_stock
                    break
            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4)

    def update_stock(self, product_name, quantity_change):
        """Update the stock level for a product. A negative value decreases stock."""
        with open(self.filename, 'r+') as f:
            data = json.load(f)
            for product_id, product_data in data['products'].items():
                if product_data['name'] == product_name:
                    product_data['stock'] += quantity_change
                    break
            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4)
    
    def update_availability(self, product_name):
        with open(self.filename, "r+") as f:
            data = json.load(f)
            for product_id, product_data in data['products'].items():
                if product_data['name'] == product_name:
                    product_data['is_available'] = product_data['stock'] > 0
                    break
            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4)



