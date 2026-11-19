from abc import ABC, abstractmethod

# Interface, no variables
class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self):
        pass
