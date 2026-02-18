# Main Menu System
while True: # This loop will repeat the menu until the user chooses the Exit option.
    # Displaying options.
    print("\n\n  ----- Welcome to your Personal Budget Calculator! -----\n")
    print("\n\n  ----- What Would You Like to Do? -----\n")
    print("    1. Track My Income and Expenses")
    print("    2. Manage My Budget")
    print("    3. View My Reports and Summaries")
    print("    4. Export/Download My Data")
    print("    5. Exit")
    option = input("\n    Please enter your option (1, 2, 3, 4): ")

    if option == "1":
        # Show menu for income entries, expense entries, and viewing transactions.
        elif option == "2":
        # Show menu for setting monthly budget limits, compare spending to budget,
        # Display warnings, and calculate remaining budget.
        elif option == "3":
        # Show menu to show total income (month), total expenses (month),
        # Calculate and display current balance (income - expenses),
        # Display expense by category, and show simple budget summary.
        elif option == "4":
        # Show menu for saving data to a text file and loading previous data when program starts,
        # Including loading it automatically, and an option to load a specific one.        
        
    # If the user inputs 5, the loop will stop and end the program.
        elif option == "5":
        print("\n    Thanks for using the VLAN Information Manager! Goodbye!")
        print("\n  ----------------------------------------------------")
        break
            else: # If the user inputs something other than 1, 2, 3, or 4, ask them again until they enter a valid number.
                print("\n    Invalid option. Please try again and enter a number between 1 and 4.")
                print("\n  ----------------------------------------------------")