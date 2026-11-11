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

# Retrieve the order lines
line_a = order_a.order_lines[0]
line_b = order_b.order_lines[0]

# Check whether they are the same OrderLine
print(line_a is line_b)

# Check whether they reference the same Product
print(line_a.product is line_b.product)

# Check whether they reference the original Product
print(line_a.product is product)

print("Before:", order_a.calculate_total())

order_a.remove_order_line(0)

print("After:", order_a.calculate_total())

# Product still exists
product.display_information()

# Order B is unaffected
print("Order B:", order_b.calculate_total())