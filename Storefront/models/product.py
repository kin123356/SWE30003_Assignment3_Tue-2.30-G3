class Product:
    def __init__(self, name, description, price, stock, is_available=True):
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.is_available = is_available

    @staticmethod
    def from_dict(data):
        return Product(
            name=data['name'],
            description=data['description'],
            price=data['price'],
            stock=data['stock'],
            is_available=data.get('is_available', True)  # Default to True for older data
        )

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stock': self.stock,
            'is_available': self.is_available
        }