# Global Constants
MAX_CAPACITY = 500

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

def main():
    # Initialize the inventory to zero in the start
    inventory = 0
    failed_entries = 0
    deliveries_processed = 0
    # Run in a continuous loop asking user to enter a stock quantity, until the user types quit.
    while True:
        # User input
        valid_stock = get_valid_input()
        # Keep running total of inventory, add valid stock
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