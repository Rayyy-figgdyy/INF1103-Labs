import json
import os

INVENTORY_FILE = "inventory.json"

# Product Class
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
    def price(self):
        return self.__price
    
    @property
    def stock(self):
        return self.__stock

    # Update stock to new quantity, return the amount changed
    def update_stock(self, quantity):
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")
        change = quantity - self.__stock
        self.__stock = quantity
        return change

    def display_information(self):
        print(
            f"ID: {self.__product_id} | "
            f"Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | "
            f"Stock: {self.__stock}"
        )

    # Convert object to dict
    def to_dict(self):
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock
        }

class Inventory:
    def __init__(self):
        self.__products = []
        self.__transactions = []

    def add_product(self, product, record_transaction=True):
        if self.search_product(product.product_id) is not None:
            return False
        self.__products.append(product)
        if record_transaction:
            self.__transactions.append({
                "type": "ADD",
                "product_id": product.product_id,
                "amount": product.stock
            })
        return True

    def search_product(self, product_id):
        for product in self.__products:
            if product.product_id == product_id:
                return product
        return None

    def update_stock(self, product_id, quantity):
        product = self.search_product(product_id)
        if product is None:
            return False
        change = product.update_stock(quantity)
        self.__transactions.append({
            "type": "UPDATE",
            "product_id": product_id,
            "amount": change
        })
        return True

    def display_all(self):
        print("\nCurrent Inventory")
        print("-" * 48)
        if not self.__products:
            print("Inventory is empty.")
        else:
            for product in self.__products:
                product.display_information()
        print("-" * 48)

    # convert object to dict
    def to_dict(self):
        return {
            "products": [product.to_dict() for product in self.__products],
            "transactions": self.__transactions
        }

    def load_transactions(self, transactions):
        self.__transactions = list(transactions)


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