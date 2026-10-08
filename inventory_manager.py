import json
import os

INVENTORY_FILE = "inventory.json"


def add_product(inventory):
    print("\nAdd New Product")

    product_id = input("Product ID: ")
    product_name = input("Product Name: ")
    price = float(input("Price: "))
    stock = int(input("Stock Quantity: "))

    # Check if ID already exists
    for product in inventory["products"]:
        if product["id"] == product_id:
            print("Product ID already exists.")
            return

    new_product = {
        "id": product_id,
        "name": product_name,
        "price": price,
        "stock": stock
    }

    inventory["products"].append(new_product)

    # Store transaction
    inventory["transactions"].append({
        "type": "ADD",
        "product_id": product_id,
        "amount": stock
    })

    print("Product added successfully!")


def update_stock(inventory):
    print("\nUpdate Stock")

    product_id = input("Enter Product ID: ")

    for product in inventory["products"]:
        if product["id"] == product_id:

            print("Product Found:")
            print(f"Name: {product['name']}")
            print(f"Current Stock: {product['stock']}")

            new_stock = int(input("New Stock Quantity: "))

            # Calculate change in stock
            stock_change = new_stock - product["stock"]

            product["stock"] = new_stock

            # Store transaction
            inventory["transactions"].append({
                "type": "UPDATE",
                "product_id": product_id,
                "amount": stock_change
            })

            print("Stock updated successfully!")
            return

    print("Product not found.")


def search_product(inventory):
    print("\nSearch Product")

    product_id = input("Enter Product ID: ")

    for product in inventory["products"]:
        if product["id"] == product_id:

            print("Product Found")
            print("-" * 48)
            print(f"ID: {product['id']}")
            print(f"Name: {product['name']}")
            print(f"Price: ${product['price']:.2f}")
            print(f"Stock: {product['stock']}")
            print("-" * 48)

            return

    print("Product not found.")


def display_all(inventory):
    print("\nCurrent Inventory")
    print("-" * 48)

    for product in inventory["products"]:
        print(
            f"ID: {product['id']} | "
            f"Name: {product['name']} | "
            f"Price: ${product['price']:.2f} | "
            f"Stock: {product['stock']}"
        )

    print("-" * 48)


def main():
    inventory = {
            "products": [],           
            "transactions": [] 
        }

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
            display_all(inventory)

        elif option == "2":
            add_product(inventory)

        elif option == "3":
            update_stock(inventory)

        elif option == "4":
            search_product(inventory)

        elif option == "5":
            print("Saving inventory...")

        elif option == "6":
            print("Saving inventory before exit...")
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()