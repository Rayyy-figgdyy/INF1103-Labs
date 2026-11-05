from Product import Product
from CanBeShipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    """A physical product with weight-based shipping."""

    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = float(weight)
        if self.__weight < 0:
            raise ValueError("Weight cannot be negative.")

    @property
    def weight(self):
        return self.__weight

    def display_information(self):
        super().display_information()
        print(f"Weight: {self.__weight:.2f} kg")

    def get_fulfilment_info(self):
        return "This product requires physical shipping."

    def calculate_shipping_cost(self):
        # Simple lab example: SGD 2 per kilogram.
        return self.__weight * 2.0

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data
