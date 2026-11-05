import json
import os
from Inventory import Inventory
from PhysicalProduct import PhysicalProduct
from DigitalProduct import DigitalProduct
from CanBeShipped import CanBeShipped

INVENTORY_FILE = "inventory.json"


def load_inventory():
    inventory = Inventory()

    if os.path.exists(INVENTORY_FILE):
        print("inventory.json found.")

        with open(INVENTORY_FILE, "r") as file:
            data = json.load(file)

        for item in data.get("products", []):

            product_type = item.get("type", "physical")

            if product_type == "physical":
                product = PhysicalProduct(
                    item["id"],
                    item["name"],
                    item["price"],
                    item["stock"],
                    item.get("weight", 0.0)
                )

            elif product_type == "digital":
                product = DigitalProduct(
                    item["id"],
                    item["name"],
                    item["price"],
                    item["stock"],
                    item.get("download_size", 0.0)
                )

            else:
                print(f"Unknown product type: {product_type}")
                continue

            inventory.add_product(
                product,
                record_transaction=False
            )

        inventory.load_transactions(
            data.get("transactions", [])
        )

        print("Inventory loaded successfully.")

    else:
        print("inventory.json not found.")
        print("Starting with empty inventory.")

    return inventory


def save_inventory(inventory):
    with open(INVENTORY_FILE, "w") as file:
        json.dump(inventory.to_dict(), file, indent=4)
    print("Inventory saved successfully to inventory.json.")


def add_product_menu(inventory):
    print("\nAdd New Product")
    print("1. Physical Product")
    print("2. Digital Product")
    product_type = input("Select product type: ").strip()
    if product_type not in ("1", "2"):
        print("Invalid product type.")
        return

    product_id = input("Product ID: ").strip()
    product_name = input("Product Name: ").strip()
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
        if product_type == "1":
            weight = float(input("Weight (kg): "))
            product = PhysicalProduct(product_id, product_name, price, stock, weight)
        else:
            download_size = float(input("Download Size (MB): "))
            product = DigitalProduct(product_id, product_name, price, stock, download_size)
    except ValueError as error:
        print(f"Invalid product information: {error}")
        return

    if inventory.add_product(product):
        print("Product added successfully!")
    else:
        print("Product ID already exists.")


def update_stock_menu(inventory):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ")
    product = inventory.search_product(product_id)
    if product is None:
        print("Product not found.")
        return
    print("Product Found:")
    print(f"Name: {product.name}")
    print(f"Current Stock: {product.stock}")
    try:
        quantity = int(input("New Stock Quantity: "))
        if quantity < 0:
            print("Stock cannot be negative.")
            return
    except ValueError:
        print("Invalid stock quantity.")
        return
    inventory.update_stock(product_id, quantity)
    print("Stock updated successfully!")


def search_product_menu(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ")
    product = inventory.search_product(product_id)
    if product is None:
        print("Product not found.")
        return
    print("Product Found")
    print("-" * 48)
    product.display_information()
    print(product.get_fulfilment_info())
    print("-" * 48)

def calculate_shipping_menu(inventory):
    print("\nCalculate Shipping Cost")

    product_id = input("Enter Product ID: ")
    product = inventory.search_product(product_id)

    if product is None:
        print("Product not found.")
        return

    if isinstance(product, CanBeShipped):
        shipping_cost = product.calculate_shipping_cost()
        print(f"Shipping Cost: ${shipping_cost:.2f}")
    else:
        print("This product does not require physical shipping.")

def main():
    inventory = load_inventory()
    while True:
        print("\n----------- MENU -----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Calculate Shipping Cost")
        print("6. Save Inventory")
        print("7. Exit")
        print("----------------------------")
        option = input("Enter option: ")
        if option == "1":
            inventory.display_all()
        elif option == "2":
            add_product_menu(inventory)
        elif option == "3":
            update_stock_menu(inventory)
        elif option == "4":
            search_product_menu(inventory)
        elif option == "5":
            calculate_shipping_menu(inventory)
        elif option == "6":
            print("Saving inventory...")
            save_inventory(inventory)
        elif option == "7":
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
