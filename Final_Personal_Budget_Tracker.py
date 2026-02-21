# Python Final Project - Personal Budget Calculator
print("Hello World!")
print("hi")


# HELLO EVERYONE PLEASE PUT YOUR CODE UNDER THIS LINE


# Displaying the Main Menu and calling the functions based on what the user enters.
def main():
    # These are the shared data structures.
    all_transactions = []
    
    # Setting monthly budget limits for expense categories.
    # Setting 0 as a placeholder. (DECIDE TOGETHER ON BUDGET)
    budget_limits = {"Food": 0, "Transportation": 0, "Entertainment": 0, "Bills": 0}
    
    # Main Menu System
    while True:
        # Displaying options.
        print("\n\n  ----- Welcome to your Personal Budget Tracker! -----\n")
        print("\n\n  ----- What Would You Like to Do? -----\n")
        print("    1. Add Income")
        print("    2. Add Expense")
        print("    3. View All Transactions")
        print("    4. Set Budget")
        print("    5. View Budget Summary")
        print("    6. Generate Report")
        print("    7. Save and Exit")
        option = input("\n    Please enter your option (1, 2, 3, 4, 5, 6, 7): ")

        if option == "1":
                print("\n ADDING INCOME FUNCTION WILL BE CALLED (KAMSI)")
            
        elif option == "2":
            print("\n ADDING EXPENSE FUNCTION WILL BE CALLED (KAMSI)")
            
        elif option == "3":
            print("\n VIEWING TRANSACIONS FUNCTION WILL BE CALLED (KAMSI)")
            
        elif option == "4":
            print("\n SETTING THE MONTHLY? BUDGET FUNCTION WILL BE CALLED (HEBA)")
            
        elif option == "5":
            print("\n VIEWING BUDGET SUMMARY FUNCTION WILL BE CALLED (HEBA)")
                
        elif option == "6":
            print("\n GENERATING REPORT FUNCTION WILL BE CALLED (ZARA)")
            
        # If the user inputs 7, the loop will stop and end the program.
        elif option == "7":
            print("\n    Thanks for using the Personal Budget Tracker! Goodbye!")
            print("\n  ----------------------------------------------------")
            break
        else: # If the user inputs something other than 1, 2, 3, or 4, ask them again until they enter a valid number.
            print("\n    Invalid option. Please try again and enter a number between 1 and 7.")
            print("\n  ----------------------------------------------------")

# Running the program.
if __name__ == "__main__":
    main()