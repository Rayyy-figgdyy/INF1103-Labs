from Product import Product
from CanBeShipped import CanBeShipped
from Supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):
    """A physical product with weight-based shipping."""

    def __init__(self, product_id: str, name: str, price: float, stock: int, weight: float, supplier: Supplier):
        super().__init__(product_id, name, price, stock, supplier)
        self.__weight = float(weight)
        if self.__weight < 0:
            raise ValueError("Weight cannot be negative.")

    @property
    def weight(self) -> float:
        return self.__weight

    def display_information(self) -> float:
        super().display_information()
        print(f"Weight: {self.__weight:.2f} kg")

    def get_fulfilment_info(self) -> str:
        return "This product requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        # $2 per kg
        return self.__weight * 2.0

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data
