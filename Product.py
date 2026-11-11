from abc import ABC, abstractmethod
from Supplier import Supplier

class Product(ABC):
    """Abstract base class for all inventory products."""

    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier):
        self.__product_id = product_id
        self.__name = name
        self.__price = float(price)
        self.__stock = int(stock)
        self.__supplier: Supplier = supplier
        if self.__price < 0 or self.__stock < 0:
            raise ValueError("Price and stock cannot be negative.")

    @property
    def product_id(self) -> str:
        return self.__product_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def price(self) -> float:
        return self.__price

    @property
    def stock(self) -> int:
        return self.__stock

    @property
    def supplier(self) -> Supplier:
        return self.__supplier

    def update_stock(self, quantity) -> int:
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")
        change = quantity - self.__stock
        self.__stock = quantity
        return change

    def display_information(self) -> None:
        print(
            f"ID: {self.__product_id} | "
            f"Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | "
            f"Stock: {self.__stock}"
        )

    @abstractmethod
    def get_fulfilment_info(self) -> None:
        """Return how this product is delivered to the customer."""
        pass

    def to_dict(self) -> dict:
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
        }
