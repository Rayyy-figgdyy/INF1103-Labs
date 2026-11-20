import csv
import json
import os
from Inventory import Inventory
from ProductFactory import ProductFactory
from CanBeShipped import CanBeShipped
from Supplier import Supplier

INVENTORY_FILE = "inventory.json"
default_supplier = Supplier(
    supplier_id = "S000",
    name = "Unknown Supplier",
    contact_email = "Unknown@example.com"
)

def load_inventory():
    inventory = Inventory()

    if os.path.exists(INVENTORY_FILE):
        print("inventory.json found.")

        with open(INVENTORY_FILE, "r") as file:
            data = json.load(file)

        for item in data.get("products", []):

            supplier_data = item.get("supplier")
            if supplier_data is None:
                supplier = default_supplier
            else:
                supplier = Supplier(
                    supplier_id = supplier_data["supplier_id"],
                    name = supplier_data["supplier_name"],
                    contact_email = supplier_data["contact_email"]
                )

            product_type = item.get("type", "physical")

            try:
                product = ProductFactory.create(
                    product_type=product_type,
                    product_id=item["id"],
                    name=item["name"],
                    price=item["price"],
                    stock_quantity=item["stock"],
                    supplier=supplier,
                    weight=item.get("weight", 0.0),
                    download_size=item.get("download_size", 0.0)
                )
            except ValueError as error:
                print(f"Invalid product information: {error}")
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


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    try:
        file = open(path, newline="", encoding="utf-8-sig")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        loaded = 0
        with file:
            reader = csv.reader(file)
            next(reader, None)  # Skip the header row.
            for row_number, row in enumerate(reader, start=2):
                try:
                    product_type, product_id, name, price, stock_quantity = row
                    product = ProductFactory.create(
                        product_type=product_type.strip(),
                        product_id=product_id.strip(),
                        name=name.strip(),
                        price=float(price),
                        stock_quantity=int(stock_quantity),
                        supplier=supplier
                    )
                except ValueError as error:
                    print(f"Skipping row {row_number}: {error}")
                    continue

                if inventory.add_product(product):
                    loaded += 1
                else:
                    print(f"Skipping row {row_number}: Product ID already exists.")

        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")


def save_inventory(inventory):
    with open(INVENTORY_FILE, "w") as file:
        json.dump(inventory.to_dict(), file, indent=4)
    print("Inventory saved successfully to inventory.json.")


def get_positive_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))

            if value <= 0:
                print("Please enter a number greater than zero.")
                continue

            return value

        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def add_product_menu(inventory):
    print("\nAdd New Product")
    print("1. Physical Product")
    print("2. Digital Product")
    print("3. Back")
    product_type = input("Select product type: ").strip()
    if product_type in ("1", "2"):
        product_id = input("Product ID: ").strip()
        product_name = input("Product Name: ").strip()
        supplier_id = input("Supplier ID: ").strip()
        supplier_name = input("Supplier Name: ").strip()
        supplier_contact_email = input("Supplier Contact Email: ").strip()
        supplier = Supplier(supplier_id, supplier_name, supplier_contact_email)  
        try:
            price = get_positive_float("Price: ")
            stock = int(input("Stock Quantity: "))
            if product_type == "1":
                weight = float(input("Weight (kg): "))
                product = ProductFactory.create(
                    "physical", product_id, product_name, price, stock,
                    supplier, weight=weight
                )
            else:
                download_size = float(input("Download Size (MB): "))
                product = ProductFactory.create(
                    "digital", product_id, product_name, price, stock,
                    supplier, download_size=download_size
                )
        except ValueError as error:
            print(f"Invalid product information: {error}")
            return

        if inventory.add_product(product):
            print("Product added successfully!")
        else:
            print("Product ID already exists.")

    elif product_type == "3":
        return

    else:
        print("Invalid product type.")
        return


def remove_product_menu(inventory):
    print("\nRemove Product")
    product_id = input("Enter Product ID: ").strip()
    if inventory.remove_product(product_id):
        print("Product removed successfully!")
    else:
        print("Product not found.")


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
        print("7. Remove Product")
        print("8. Exit")
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
            remove_product_menu(inventory)
        elif option == "8":
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
