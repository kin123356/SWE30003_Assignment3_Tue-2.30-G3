class Product:
    def __init__(self, name, description, price, stock):
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock

    @classmethod
    def from_dict(cls, data):
        return cls(data['name'], data['description'], data['price'], data['stock'])

    def to_dict(self):
        return{
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock
        }