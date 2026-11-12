from Supplier import Supplier
from PhysicalProduct import PhysicalProduct
from DigitalProduct import DigitalProduct
from Inventory import Inventory

supplier = Supplier(
    "S001", "ABC Supplies", "abc@example.com"
)

physical = PhysicalProduct(
    "P001", "Laptop", 1200, 10, 2.5, supplier
)

digital = DigitalProduct(
    "D001", "Software", 99, 50, 500, supplier
)

inventory = Inventory()

inventory.add_product(physical)
inventory.add_product(digital)

inventory.display_all()