# Initialize the inventory to zero in the start
inventory = 0

# Run in a continuous loop asking user to enter a stock quantity, until the user types quit.
while True:
    stock_input = input("Enter stock quantity (or enter 'quit' to exit program): ")

    # Exit the program if user types quit
    if stock_input.lower() == "quit":
        break

