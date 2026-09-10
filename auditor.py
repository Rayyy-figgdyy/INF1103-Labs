# Initialize the inventory to zero in the start
inventory = 0

# Run in a continuous loop asking user to enter a stock quantity, until the user types quit.
while True:
    stock_input = input("Enter stock quantity (or enter 'quit' to exit program): ")

    # Exit the program if user types quit
    if stock_input.lower() == "quit":
        break

    # Handling invalid inputs
    # Check if input contains only digits
    # Reject negative numbers
    if not stock_input.isdigit() or stock_input < 0:
        print("Error: Invalid input, please enter a positive whole number.")

        continue
    
    # Convert input to int if valid
    stock = int(stock_input)
