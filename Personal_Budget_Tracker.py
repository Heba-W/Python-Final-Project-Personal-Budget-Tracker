# Python Final Project - Personal Budget Calculator
class Transaction:
    def __init__(self, t_type, category, description, amount):
        self.t_type = t_type # Income or Expense
        self.category = category        # "Food", "Bills", "Salary", etc.
        self.description = description
        self.amount = amount


income_info = {} 
expense_cat = {
    1: "Food",
    2: "Transportation",
    3: "Entertainment",
    4: "Bills",
    5: "Other"
}
# Setting monthly budget limits for expense categories.
# Setting 0 as a placeholder. Changes when user inputs something else.
budget_limits = {"Food": 0, "Transportation": 0, "Entertainment": 0, "Bills": 0}

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

def view_budget_summary(budget_limits, expense_list):
    print("\n--- Monthly Budget Summary ---")
    print(f"{'Category':<15} | {'Budget':<10} | {'Spent':<10} | {'Remaining':<10}")
    print("-" * 55)
    
    # Dictionary to keep track of totals per category
    totals = {cat: 0 for cat in budget_limits}
    
    # Adding up the expenses
    for item in expense_list:
        cat = item.category
        if cat in totals:
            totals[cat] += item.amount
    
    # Display the math
    for cat, limit in budget_limits.items():
        spent = totals[cat]
        remaining = limit - spent
        
        # Warning when approaching or exceeding limits
        status = ""
        if spent > limit and limit > 0:
            status = "!! OVER BUDGET !!"
        elif spent >= limit * 0.9 and limit > 0:
            status = "* Close to limit *"

        print(f"{cat:<15} | ${limit:>8.2f} | ${spent:>8.2f} | ${remaining:>9.2f}  {status}")

# Displaying the Main Menu and calling the functions based on what the user enters.
def main():
    # These are the shared data structures.
    all_transactions = []
    income = []
    expense = []
    
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
            add_income(income)
            
        elif option == "2":
            add_expense(expense, budget_limits)
            
        elif option == "3":
            view_transactions(income, expense)
            
        elif option == "4":
            print("\n SETTING THE MONTHLY BUDGET FUNCTION WILL BE CALLED (HEBA)")
            setting_budget(budget_limits)
            
        elif option == "5":
            print("\n VIEWING BUDGET SUMMARY FUNCTION WILL BE CALLED (KAMSI AND HEBA)")
            view_budget_summary(budget_limits, expense)
            
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

            

def add_income(income_list):
    print("You have selected the Add Income option.\nEnter your details below")
    
    description = input("Enter income description: ")
    try:
        amount = float(input("Enter the amount: "))

        # 2. Simplified logic: if amount is valid, save it. 
        if amount >= 1:
            # 3. Use the list passed into the function (income_list) 
            # and the Class blueprint
            new_income = Transaction("Income", "N/A", description, amount)
            income_list.append(new_income)
            print("Income added successfully!") 
        else:
            print("Error: Amount must be at least $1.00. Transaction cancelled.")
            
    except ValueError:
        print("Error: Please enter a valid number for the amount.")

    print("\n")
    enter = input("Press the Enter key to continue...")
    if enter == "":
        print("Continuing...")
        print("\n")


def add_expense(expense, budget_limits):
    print("Select a category. Choose an option from 1-5\n ")
    
    for key, value in expense_cat.items():
        print(f"{key}. {value}")
    
    user_input = int(input("Enter category"))

    if user_input in expense_cat:
        expense_description = str(input("Enter expense description: "))
        expense_amount = float(input("Enter the amount: "))
        # Create the object using your class blueprint
        new_expense = Transaction("Expense", expense_cat[user_input], expense_description, expense_amount)
        expense.append(new_expense)
        
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

def view_transactions(income_list, expense_list):
    print("\n--- VIEWING ALL TRANSACTIONS ---")
    print("\n[ Income Transactions ]")
    if not income:
        print("No income recorded yet.")
    else:
        for item in income:
            print(f"- {item.description}: ${item.amount:.2f}")

    print("\n[ Expense Transactions ]")
    if not expense:
        print("No expenses recorded yet.")
    else:
        for item in expense:
            print(f"- {item.category} ({item.description}): ${item.amount:.2f}")
    print("\n" + "-"*30)
    input("Press the Enter key to continue...")

# def option_view(income, expense):
#     print("You have selected the View All Transactions options")
#     print("These are your income inputs saved:", *income)
#     print("\n")
#     print("These are your saved expense inputs:",*expense)
#     user_input = input("Press the Enter key to continue: ")
#     if user_input == "":
#         print("Continuing...")
#         print("\n")
        
# Running the program.
if __name__ == "__main__":
    main()
