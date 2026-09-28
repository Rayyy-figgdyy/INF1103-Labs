# Global Constants
MAX_CAPACITY = 500
INVENTORY_FILE = "inventory.txt"

def get_valid_input():
    stock_input = input("Enter stock quantity (or enter 'quit' to exit program): ")

    # Exit the program if user types quit
    if stock_input.lower() == "quit":
        return "quit"

    # Handling invalid inputs
    # Check if input contains only digits
    # Reject negative numbers
    if not stock_input.isdigit() or int(stock_input) < 0:
        print("Error: Invalid input, please enter a positive whole number.")
        return "invalid number"
    
    # Convert input to int if valid
    stock = int(stock_input)
    return stock


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
            generate_report(inventory, failed_entries)
            break

        # Count invalid entries
        elif valid_stock == "invalid number":
            failed_entries += 1

        # Process valid delivery
        else:
            # Update inventory
            inventory = process_delivery(inventory, valid_stock)

            # Calculate tax for delivery
            tax = calculate_tax(valid_stock)

            # Count valid delivery
            deliveries_processed += 1

        # Overstock alert
        if inventory > MAX_CAPACITY:
            print("ALERT: Inventory exceeds 500 units!")
            generate_report(inventory, failed_entries)
            break


# Program Entry Point
if __name__=="__main__":
    main()