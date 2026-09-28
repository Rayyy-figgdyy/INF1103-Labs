# Global Constants
MAX_CAPACITY = 500
INVENTORY_FILE = "inventory.txt"


def get_valid_input():
    # Get product name
    prod_name = input("Enter Product Name (or enter 'quit' to exit program): ")

    # Exit the program if user types quit
    if prod_name.lower() == "quit":
        return "quit"

    # Get quantity
    quantity_input = input("Enter Quantity: ")

    # Handling invalid inputs
    # Check if input contains only digits
    # Reject negative numbers
    if not quantity_input.isdigit() or int(quantity_input) < 0:
        print("Error: Invalid quantity, please enter a positive whole number.")
        return "invalid number"

    # Convert quantity to int
    quantity = int(quantity_input)

    # Return product name and quantity
    return prod_name, quantity


def generate_report(inventory_units, failed_entries):
    print("\nInventory Report:")
    print(f"Total Deliveries Processed: {inventory_units}")
    print(f"Number of Failed/Rejected Entries: {failed_entries}")


def process_delivery(current_total, new_value): 
    new_total = current_total + new_value
    return new_total


def calculate_tax(amount):
    tax = amount * 0.1
    return tax


def load_inventory():
    try:
        with open(INVENTORY_FILE, "r") as file:

            # Read the first line (Total)
            total_line = file.readline().strip()
            inventory = int(total_line.split(":")[1].strip())

            # Read the History line
            history_line = file.readline().strip()

            transactions = []

            if history_line.startswith("History:"):
                # Remove "History:" from the beginning
                history_line = history_line.replace("History: ", "").strip()

                # Split each transaction
                transaction_list = history_line.split("],[")

                for transaction in transaction_list:
                    # Remove brackets
                    transaction = transaction.strip("[]")

                    # Split into ID, product name and quantity
                    items = transaction.split(",")

                    product_id = int(items[0].strip())
                    product_name = items[1].strip().strip("'")
                    quantity = int(items[2].strip())

                    transactions.append(
                        [product_id, product_name, quantity]
                    )

            return inventory, transactions

    except FileNotFoundError:
        return 0, []


def save_inventory(inventory, transaction_history):
    # Saves the current inventory total and transaction history to inventory.txt.
    with open(INVENTORY_FILE, "w") as file:
        file.write(f"Total: {inventory}\n")
        history = ",".join(str(value) for value in transaction_history)
        file.write(f"History: {history}")


def main():

    failed_entries = 0
    deliveries_processed = 0

    # Load previous inventory and transaction history
    inventory, transaction_history = load_inventory()
    
    # Show transaction history
    print(f"Current inventory: {inventory} units")
    print(f"Previous transactions: ")
    for transaction in transaction_history:
        product_id, product_name, quantity = transaction
        print(f"{product_id}, {product_name}, {quantity}")

    # Determine the next product ID
    if transaction_history:
        next_product_id = int(transaction_history[-1][0]) + 1
    else:
        next_product_id = 1001

    # Run until the user types quit.
    while True:

        # User input
        valid_stock = get_valid_input()

        # User quit 
        if valid_stock == "quit":

            # Save inventory and transaction history
            save_inventory(inventory, transaction_history)

            # Generate report
            generate_report(inventory, failed_entries)

            break

        # Count invalid entries
        elif valid_stock == "invalid number":
            failed_entries += 1

        # Process valid delivery
        else:
            # Separate product name and quantity
            product_name = valid_stock[0]
            quantity = valid_stock[1]

            # Update inventory
            inventory = process_delivery(inventory, quantity)

            # Add entry to transaction history
            transaction_entry = [next_product_id, product_name, quantity]
            transaction_history.append(transaction_entry)
            print("\nNew Order Added:")
            print(f"{next_product_id}, {product_name}, {quantity}")
            next_product_id += 1

            # Calculate tax for delivery
            tax = calculate_tax(valid_stock[1])

            # Count valid delivery
            deliveries_processed += 1

            # print(f"Delivery accepted: {valid_stock[0]}, {valid_stock[1]} units")
            # print(f"Tax for this delivery: ${tax:.2f}")
            print(f"Current inventory: {inventory} units\n")

        # Overstock alert
        if inventory > MAX_CAPACITY:
            print("ALERT: Inventory exceeds 500 units!")

            # Save before exiting so the latest transaction is not lost
            save_inventory(inventory, transaction_history)

            generate_report(inventory, failed_entries)
            
            break


# Program Entry Point
if __name__=="__main__":
    main()