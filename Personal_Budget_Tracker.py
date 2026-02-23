income_info = {} 
income = []     
expense_cat = {
    1: "Food",
    2: "Transportation",
    3: "Entertainment",
    4: "Bills",
    5: "Other"
}
budget_limits = {"Food": 0, "Transportation": 0, "Entertainment": 0, "Bills": 0}
expense = []
# Python Final Project - Personal Budget Calculator
print("Hello World!")

# HELLO EVERYONE PLEASE PUT YOUR CODE UNDER THIS LINE


# Budget Managment Functions
# Function to Set a Monthly Budget
def setting_budget(budget_limits):
    print(" --- Set Monthly Budget ---")
    print("Categories: Food, Transportation, Entertainment, Bills")
    
    # Asking the user which category they want to set a budget for, and storing it.
    category = input("Please enter the category you want to set a budget for: ").capitalize()
    
    # Checking if the category exists in the dictionary
    if category in budget_limits:
        try:
            # Ask for the limit and convert/store it as a float.
            amount = float(input(f"Enter the budget amount for {category}: "))
            budget_limits[category] = amount
            print(f"Adding the budget was successful! The monthly budget for {category} is now ${amount:.2f}")
        except ValueError:
            print("Invalid input. Please try again and enter a numeric value for the budget amount.")
    else:
        print("That category does not exist. Please try again.")


# Displaying the Main Menu and calling the functions based on what the user enters.
def main():
    # These are the shared data structures.
    all_transactions = []
    
    # Setting monthly budget limits for expense categories.
    # Setting 0 as a placeholder. Changes when user inputs something else.
   
    
    # Main Menu System
    while True:
        # Displaying options.
        print("\n\n  ----- Welcome to your Personal Budget Tracker! -----")
        print("\n  ----- What Would You Like to Do? -----\n")
        print("    1. Add Income")
        print("    2. Add Expense")
        print("    3. View All Transactions")
        print("    4. Set a Monthly Budget")
        print("    5. View Budget Summary")
        print("    6. Generate Report")
        print("    7. Save and Exit")
        option = input("\n    Please enter your option (1, 2, 3, 4, 5, 6, 7): ")

        if option == "1":
            option_income()
            
        elif option == "2":
            option_expense()
            
        elif option == "3":
            option_view()
            
        elif option == "4":
            print("\n SETTING THE MONTHLY BUDGET FUNCTION WILL BE CALLED (HEBA)")
            setting_budget(budget_limits)
            
        elif option == "5":
            print("\n VIEWING BUDGET SUMMARY FUNCTION WILL BE CALLED (KAMSI AND HEBA)")
                
        elif option == "6":
            print("\n GENERATING REPORT FUNCTION WILL BE CALLED (ZARA)")
            
        # If the user inputs 7, the loop will stop and end the program.
        elif option == "7":
            print("\n    Thanks for using the Personal Budget Tracker! Goodbye!")
            print("\n  ----------------------------------------------------")
            break
        else:
            # If the user inputs something other than 1–7
            print("\n    Invalid option. Please try again and enter a number between 1 and 7.")
            print("\n  ----------------------------------------------------")

            

def option_income():
    print("You have selected the Add Income option.\nEnter your details below")
    
    income_info["description"] = str(input("Enter income description: "))
    income_info["amount"] = float(input("Enter the amount: "))

    if income_info["amount"] >= 1:
        print(" Income added successfully!") 
    else:
        print("Number cannot be less than 1. Type out your amount once more!")
        income_info["amount"] = float(input("Enter the amount: "))
        print("Income added successfully!") 

    income.append(income_info.copy())

    print("\n")
    
    user_input = input("Press the Enter key to continue: ")
    if user_input == "":
        print("Continuing...")
        print("\n")


def option_expense():
    print("Select a category. Choose an option from 1-5\n ")
    
    for key, value in expense_cat.items():
        print(f"{key}. {value}")
    
    user_input = int(input("Enter category"))

    if user_input in expense_cat:
        expense_description = str(input("Enter expense description: "))
        expense_amount = float(input("Enter the amount: "))
        expense.append({
            "category": expense_cat[user_input],
            "description": expense_description,
            "amount": expense_amount
        })
        remaining_food_budget(budget_limits, expense)
        print("Expense added successfully!")
        
    else:
        print("Invalid category.")
        user_input = int(input("Enter category"))
        expense_description = str(input("Enter expense description: "))
        expense_amount = float(input("Enter the amount: "))
        expense.append({
            "category": expense_cat[user_input],
            "description": expense_description,
            "amount": expense_amount
        })
        print("Expense added successfully!")

    print("\n")
    
    user_input = input("Press the Enter key to continue: ")
    if user_input == "":
        print("Continuing...")
        print("\n")

def remaining_food_budget(budget_limits, expense):
    food_budget = budget_limits["Food"]
    
    total_food_spent = 0
    for item in expense:
        if item["category"] == "Food":
            total_food_spent += item["amount"]
    
    remaining = food_budget - total_food_spent
    
    print(f"Food Budget: ${food_budget}")
    print(f"Total Spent on Food: ${total_food_spent}")
    print(f"Remaining Food Budget: ${remaining}")


def option_view():
    print("You have selected the View All Transactions options")
    print("These are your income inputs saved:", *income)
    print("\n")
    print("These are your saved expense inputs:",*expense)
    user_input = input("Press the Enter key to continue: ")
    if user_input == "":
        print("Continuing...")
        print("\n")
        
# Running the program.
if __name__ == "__main__":
    main()
