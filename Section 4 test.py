from Supplier import Supplier
from PhysicalProduct import PhysicalProduct
from Order import Order

# Create a supplier
supplier = Supplier("S001", "ABC Supplies", "abc@example.com")

# Create one product
product = PhysicalProduct(
    "P001", "Laptop", 1200, 10, 2.5, supplier
)

# Create two orders
order_a = Order("O001")
order_b = Order("O002")

# Add the same product to both orders
order_a.add_order_line(product, 2)
order_b.add_order_line(product, 3)

# Calculate totals
print("Order A total:", order_a.calculate_total())
print("Order B total:", order_b.calculate_total())