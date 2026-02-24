###### Python Final Project - Personal Budget Calculator

import os
from datetime import datetime

class Transaction:
    def __init__(self, t_type, category, description, amount):
        self.t_type = t_type # Income or Expense
        self.category = category        # "Food", "Bills", "Salary", etc.
        self.description = description
        self.amount = amount
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M")
        
    def display_info(self):
        if self.t_type == "Income":
            return f"{self.date} | [INCOME] {self.description:<15} : ${self.amount:>8.2f}"
        return f"{self.date} | [{self.category:<12}] {self.description:<15} : ${self.amount:>8.2f}"

expense_cat = {
    1: "Food",
    2: "Transportation",
    3: "Entertainment",
    4: "Bills",
    5: "Other"
}
# Monthly budget limits for expense categories. 0 is placeholder. Changes when user inputs something else.
budget_limits = {"Food": 0, "Transportation": 0, "Entertainment": 0, "Bills": 0, "Other": 0}

# Function to add income
def add_income(transactions):
    print("You have selected the Add Income option.\nEnter your details below")
    
    description = input("Enter income description: ")
    try:
        amount = float(input("Enter the amount: "))

        # 2. Simplified logic: if amount is valid, save it. 
        if amount >= 1:
            # 3. Use the list passed into the function (income_list) 
            # and the Class blueprint
            new_income = Transaction("Income", "N/A", description, amount)
            transactions.append(new_income)
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

# Function to add expense
def add_expense(transactions, budget_limits):
    print("\n--- Add Expense ---")
    for key, value in expense_cat.items():
        print(f"{key}. {value}")
    try:
        choice = int(input("Select a category (1-5): "))
        if choice in expense_cat:
            desc = input("Enter expense description: ")
            amt = float(input("Enter amount: "))
            if amt > 0:
                # Use the Transaction class as required by rubric
                new_expense = Transaction("Expense", expense_cat[choice], desc, amt)
                transactions.append(new_expense)
                print(f"Successfully added ${amt:.2f} to {expense_cat[choice]}!")
                
                # Check budget for this specific category (Task 3 requirement)
                check_category_limit(expense_cat[choice], budget_limits, transactions)
            else:
                print("Amount must be positive.")
        else:
            print("Invalid category.")
    except ValueError:
        print("Error: Please enter numbers only for category and amount.")
    
    input("\nPress Enter to continue...")

def check_category_limit(category, budget_limits, transactions):
    if category in budget_limits and budget_limits[category] > 0:
        total_spent = sum(item.amount for item in transactions if item.t_type == "Expense" and item.category == category)
        
        limit = budget_limits[category]
        
        if total_spent > limit:
            print(f"!!! WARNING: You have exceeded your {category} budget by ${total_spent - limit:.2f} !!!")
        elif total_spent >= limit * 0.9:
            print(f"*** CAUTION: You have used { (total_spent/limit)*100 :.1f}% of your {category} budget ***")

# Function to Set a Monthly Budget
def setting_budget(budget_limits):
    print("\n--- Set Monthly Budget ---")
    # Display numbered categories (reuse your expense_cat dictionary)
    for key, value in expense_cat.items():
        print(f"{key}. {value}")
    try:
        choice = int(input("Select a category to set a budget for (1-5): "))
        if choice in expense_cat:
            category = expense_cat[choice]
            
            amount = float(input(f"Enter the monthly budget for {category}: $"))
            
            if amount >= 0:
                budget_limits[category] = amount
                print(f"Budget for {category} successfully set to ${amount:.2f}")
            else:
                print("Budget must be zero or greater.")
        else:
            print("Invalid category selection.")
    except ValueError:
        print("Error: Please enter numeric values only.")
    input("\nPress Enter to continue...")

def view_budget_summary(budget_limits, transactions):
    print("\n--- Monthly Budget Summary ---")
    print(f"{'Category':<15} | {'Budget':<10} | {'Spent':<10} | {'Remaining':<10}")
    print("-" * 55)
    
    # Calculating totals
    totals = {cat: 0 for cat in budget_limits}

    for item in transactions:
        if item.t_type == "Expense" and item.category in totals:
            totals[item.category] += item.amount
    
    # Display the math
    for cat, limit in budget_limits.items():
        spent = totals[cat]
        remaining = limit - spent
        
        # Warning when approaching (around 90%) or exceeding limits
        status = ""
        if limit > 0:
            if spent > limit:  
                status = "!! OVER BUDGET !!"
            elif spent >= limit * 0.9:
                status = f"* Warning: You have reached 90% of your budget. *"

        print(f"{cat:<15} | ${limit:>8.2f} | ${spent:>8.2f} | ${remaining:>9.2f}  {status}")

# Function to view transactions
def view_transactions(transactions):
    print("\n--- VIEWING ALL TRANSACTIONS ---")
    print("\n[ Income Transactions ]")
    found_income = False
    for item in transactions:
        if item.t_type == "Income":
            print(item.display_info())
            found_income = True
    if not found_income:
        print("No income recorded yet.")

    print("\n[ Expense Transactions ]")
    found_expense = False
    for item in transactions:
        if item.t_type == "Expense":
            print(item.display_info())
            found_expense = True
    if not found_expense:
        print("No expenses recorded yet.")
        
    print("\n" + "-"*30)
    input("Press the Enter key to continue...")

        
# Displaying the Main Menu and calling the functions based on what the user enters.
def main():
    # These are the shared data structures.
    transactions = []
    
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
            add_income(transactions)
            
        elif option == "2":
            add_expense(transactions, budget_limits)
            
        elif option == "3":
            view_transactions(transactions)
            
        elif option == "4":
            print("\n SETTING THE MONTHLY BUDGET FUNCTION WILL BE CALLED (HEBA)")
            setting_budget(budget_limits)
            
        elif option == "5":
            print("\n VIEWING BUDGET SUMMARY FUNCTION WILL BE CALLED (KAMSI AND HEBA)")
            view_budget_summary(budget_limits, transactions)
            
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

# Running the program.
if __name__ == "__main__":
    main()
