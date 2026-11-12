from Supplier import Supplier
from PhysicalProduct import PhysicalProduct
from Inventory import Inventory

# Create supplier
supplier = Supplier(
    "S001", "ABC Supplies", "abc@example.com"
)

# Create product independently
product = PhysicalProduct(
    "P001", "Laptop", 1200, 10, 2.5, supplier
)

# Create two inventories
inventory_a = Inventory()
inventory_b = Inventory()

# Add product to Inventory A
inventory_a.add_product(product)

print("Inventory A:")
inventory_a.display_all()

# Remove product from Inventory A
inventory_a.remove_product("P001")

print("\nAfter removal:")
inventory_a.display_all()

# Verify product still exists
print("\nProduct still exists:")
product.display_information()

# Add same product to Inventory B
inventory_b.add_product(product)

print("\nInventory B:")
inventory_b.display_all()