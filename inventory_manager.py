import json
import os

INVENTORY_FILE = "inventory.json"

class Product:
    """Represents one product and manages its stock."""

    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = float(price)
        self.__stock = int(stock)

    @property
    def product_id(self):
        return self.__product_id

    @property
    def name(self):
        return self.__name

    @property
    def stock(self):
        return self.__stock

    def update_stock(self, quantity):
        """Set the stock to a new quantity; return the amount changed."""
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")
        change = quantity - self.__stock
        self.__stock = quantity
        return change

    def display_information(self):
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock}")

    def to_dict(self):
        """Convert a Product object into JSON-compatible data."""
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock
        }


def load_inventory():

    if os.path.exists(INVENTORY_FILE):
        print("inventory.json found.")

        with open(INVENTORY_FILE, "r") as file:
            inventory = json.load(file)

        print("Inventory loaded successfully.")
    
    else:
        print("inventory.json not found.")
        print("Starting with empty inventory.")

        inventory = {
            "products": [],           
            "transactions": [] 
        }

    return inventory


def save_inventory(inventory):
    with open(INVENTORY_FILE, "w") as file:
        json.dump(inventory, file, indent=4)

    print("Inventory saved successfully to inventory.json.")


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

    if not inventory["products"]:
        print("Inventory is empty.")
        return

    for product in inventory["products"]:
        print(
            f"ID: {product['id']} | "
            f"Name: {product['name']} | "
            f"Price: ${product['price']:.2f} | "
            f"Stock: {product['stock']}"
        )

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
            display_all(inventory)

        elif option == "2":
            add_product(inventory)

        elif option == "3":
            update_stock(inventory)

        elif option == "4":
            search_product(inventory)

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