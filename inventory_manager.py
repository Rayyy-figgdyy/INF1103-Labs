import json
import os
from Product import Product
from Inventory import Inventory

INVENTORY_FILE = "inventory.json"


def load_inventory():
    inventory = Inventory()
    if os.path.exists(INVENTORY_FILE):
        print("inventory.json found.")
        with open(INVENTORY_FILE, "r") as file:
            data = json.load(file)
        for item in data.get("products", []):
            product = Product(item["id"], item["name"], item["price"], item["stock"])
            inventory.add_product(product, record_transaction=False)
        inventory.load_transactions(data.get("transactions", []))
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
    product_id = input("Product ID: ")
    product_name = input("Product Name: ")
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
        if price < 0 or stock < 0:
            print("Price and stock cannot be negative.")
            return
    except ValueError:
        print("Invalid price or stock quantity.")
        return
    product = Product(product_id, product_name, price, stock)
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
    print("-" * 48)


def main():
    inventory = load_inventory()
    while True:
        print("\n----------- MENU -----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")
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
            print("Saving inventory...")
            save_inventory(inventory)
        elif option == "6":
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()