from Supplier import Supplier
from PhysicalProduct import PhysicalProduct
from DigitalProduct import DigitalProduct

supplier = Supplier("S001", "ABC Supplies", "abc@example.com")

physical = PhysicalProduct(
    "P001", "Laptop", 1200, 10, 2.5, supplier
)

digital = DigitalProduct(
    "D001", "Software", 99, 50, 500, supplier
)

del supplier

physical.supplier.display_information()
digital.supplier.display_information()