from Product import Product
from OrderLine import OrderLine

class Order:
    def __init__(self, order_id: str):
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    @property
    def order_id(self) -> tuple[str]:
        return tuple(self.__order_id)
    
    @property
    def order_lines(self) -> tuple[OrderLine, ...]:
        return tuple(self.__order_lines)

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, index: int) -> bool:
        if 0 <= index < len(self.__order_lines):
            self.__order_lines.pop(index)
            return True

        return False

    def calculate_total(self) -> float:
        total = 0.0

        for order_line in self.__order_lines:
            total += order_line.calculate_subtotal()

        return total