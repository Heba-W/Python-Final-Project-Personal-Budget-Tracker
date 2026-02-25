# Python Final Project - Personal Budget Calculator

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
            return f"{self.date} | {self.description:<10} | ${self.amount:>8.2f}"
        return f"{self.date} | {self.category} | {self.description:<10} | ${self.amount:>8.2f}"

# -----------------------------
# SAVE / LOAD FUNCTIONS
# -----------------------------
DATA_FILE = "budget_data.txt"

def save_data(transactions, budget_limits):
    # """
    # Saves all financial data to a text file.
    # Sections:
    #   [BUDGET_LIMITS] -> category|limit
    #   [TRANSACTIONS]  -> type|category|description|amount|date
    # """
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            # Save budget limits
            file.write("[BUDGET_LIMITS]\n")
            for category, limit in budget_limits.items():
                file.write(f"{category}|{limit}\n")
            
            # Save all transactions (income + expense)
            file.write("[TRANSACTIONS]\n")
            for t in transactions:
                file.write(f"{t.t_type}|{t.category}|{t.description}|{t.amount}|{t.date}\n")
    except OSError as e:
        print(f"Error saving data: {e}")

def load_data(transactions, budget_limits):
    """
    Loads financial data from the file.
    Reconstructs transactions and budget limits.
    """
    if not os.path.exists(DATA_FILE):
        # Create empty data file so persistence always exists
        save_data(transactions, budget_limits)
        return

    section = None
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                if line == "[BUDGET_LIMITS]":
                    section = "BUDGET_LIMITS"
                    continue
                elif line == "[TRANSACTIONS]":
                    section = "TRANSACTIONS"
                    continue

                try:
                    if section == "BUDGET_LIMITS":
                        category, limit = line.split("|")
                        budget_limits[category] = float(limit)
                    elif section == "TRANSACTIONS":
                        t_type, category, description, amount, date = line.split("|")
                        t = Transaction(t_type, category, description, float(amount))
                        t.date = date  # restore original timestamp
                        transactions.append(t)
                except ValueError:
                    # skip corrupted lines
                    continue
    except OSError as e:
        print(f"Error loading data: {e}")

expense_cat = {
    1: "Food",
    2: "Transportation",
    3: "Entertainment",
    4: "Bills",
    5: "Other"
}

# Function to add income
def add_income(transactions, budget_limits):
    print("\n    --- Add Income ---\n    Please enter details below.\n")
    
    description = input("    Enter income description: ")
    try:
        amount = float(input("    Enter the amount: "))

        # Simplified logic: if amount is valid, save it. 
        if amount >= 1:
            # Use the list passed into the function (income_list) 
            # and the Class blueprint
            new_income = Transaction("Income", "N/A", description, amount)
            transactions.append(new_income)
            print("    Income was added successfully!")
            total_income = sum(t.amount for t in transactions if t.t_type == "Income")
            total_expense = sum(t.amount for t in transactions if t.t_type == "Expense")
            balance = total_income - total_expense
            print(f"    Current balance: ${balance:.2f}")
            save_data(transactions, budget_limits)
        else:
            print("    Error: Amount must be at least $1.00. Transaction cancelled.")      
    except ValueError:
        print("    Error: Please enter a valid number for the amount.")

    print("\n")
    enter = input("    Press the Enter key to continue...")

# Function to add expense
def add_expense(transactions, budget_limits):
    print("\n    --- Add Expense ---")
    print("    Select a Category:")
    for key, value in expense_cat.items():
        print(f"{key}. {value}")
    try:
        choice = int(input("\n    Enter a category (1-5): "))
        if choice in expense_cat:
            desc = input("    Enter expense description: ")
            amt = float(input("    Enter the amount: "))
            if amt > 0:
                # Use the Transaction class as required by rubric
                new_expense = Transaction("Expense", expense_cat[choice], desc, amt)
                transactions.append(new_expense)
                print(f"\n    Successfully added expense of ${amt:.2f} to {expense_cat[choice]}!")
                category = expense_cat[choice]
                limit = budget_limits.get(category, 0)
                if limit > 0:
                    total_spent = sum(t.amount for t in transactions if t.t_type == "Expense" and t.category == category)
                    remaining = limit - total_spent
                    print(f"    Remaining {category} budget: ${remaining:.2f}")
                
                save_data(transactions, budget_limits)
                
                # Check budget for this specific category (Task 3 requirement)
                check_category_limit(expense_cat[choice], budget_limits, transactions)
            else:
                print("    Error: Amount must be positive.")
        else:
            print("    Error: Invalid category.")
    except ValueError:
        print("    Error: Please enter numbers only for category and amount.")
    
    input("\n    Press the Enter key to continue...")

def check_category_limit(category, budget_limits, transactions):
    if category in budget_limits and budget_limits[category] > 0:
        total_spent = sum(item.amount for item in transactions if item.t_type == "Expense" and item.category == category)
        
        limit = budget_limits[category]
        
        if total_spent > limit:
            print(f"\n    !!! WARNING: You have exceeded your {category} budget by ${total_spent - limit:.2f} !!!")
        elif total_spent >= limit * 0.9:
            print(f"\n    * Caution: You have used { (total_spent/limit)*100 :.1f}% of your {category} budget. *")
        else:
            print(f"\n    * You have used { (total_spent/limit)*100 :.1f}% of your {category} budget. *")

# Function to view all transactions
def view_transactions(transactions):
    print("\n    --- View All Transactions ---")
    print("\n    - Income Transactions -")
    found_income = False
    for item in transactions:
        if item.t_type == "Income":
            print(f"    {item.display_info()}")
            found_income = True
    if not found_income:
        print("    No income recorded yet.")

    print("\n    - Expense Transactions -")
    found_expense = False
    for item in transactions:
        if item.t_type == "Expense":
            print(f"    {item.display_info()}")
            found_expense = True
    if not found_expense:
        print("    No expenses recorded yet.")
        
    print("\n    -----------------------------")
    input("\n    Press the Enter key to continue...")

# Function to Set a Monthly Budget
def setting_budget(budget_limits, transactions):
    print("\n    --- Set Monthly Budget ---")
    # Display numbered categories (reuse your expense_cat dictionary)
    for key, value in expense_cat.items():
        print(f"{key}. {value}")
    try:
        choice = int(input("    Select a category to set a budget for (1-5): "))
        if choice in expense_cat:
            category = expense_cat[choice]
            
            amount = float(input(f"    Enter the monthly budget for {category}: $"))
            
            if amount >= 0:
                budget_limits[category] = amount
                print(f"    Budget for {category} successfully set to ${amount:.2f}.")
                save_data(transactions, budget_limits)
            else:
                print("    Error: Budget must be zero or greater.")
        else:
            print("    Error: Invalid category selection.")
    except ValueError:
        print("    Error: Please enter numeric values only.")
    input("\n    Press the Enter key to continue...")

# Function to view a budget summary
def view_budget_summary(budget_limits, transactions):
    print(f"\n    --- Budget Summary for This Month ---")
    print(f"    Summary generated at: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    # Calculate total income and total expenses first
    total_income = sum(t.amount for t in transactions if t.t_type == "Income")
    total_expense = sum(t.amount for t in transactions if t.t_type == "Expense")
    current_balance = total_income - total_expense

    print(f"    INCOME:\n    Total Income: ${total_income:.2f}")
    print(f"\n    EXPENSES BY CATEGORY:\n")
    
    print(f"    {'Category':<15} | {'Budget':<9} | {'Spent':<9} | {'Remaining':<10}")
    print("    ----------------------------------------------------------")
    
    # Calculating totals for each seperate category
    totals = {cat: 0 for cat in budget_limits}
    last_entry = {cat: "N/A" for cat in budget_limits}
    # Calculate totals and track last transaction date per category
    for item in transactions:
        if item.t_type == "Expense" and item.category in totals:
            totals[item.category] += item.amount
            # Update last entry timestamp for this category
            last_entry[item.category] = item.date
    
    # Display the math
    for cat, limit in budget_limits.items():
        spent = totals[cat]
        remaining = limit - spent
        status = ""
        if limit > 0:
            if spent > limit:  
                status = "  !! Warning: You are over budget !!"
            elif spent >= limit * 0.9:
                status = f" *Warning: 90% or more used.*"
        print(f"    {cat:<15} | ${limit:>8.2f} | ${spent:>8.2f} | ${remaining:>9.2f} | {last_entry[cat]:<16} {status}")

    print(f"\n    Total Expenses: ${total_expense:.2f}")
    print(f"    Current remaining Balance: ${current_balance:.2f}")
    input("\n    Press the Enter key to continue...")
    


# Function to generate a final report
def generate_report(transactions, budget_limits):
    print("\n\n    --- Monthly Financial Report ---\n")
    print(f"    Report generated at: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # Calculate totals
    total_income = sum(t.amount for t in transactions if t.t_type == "Income")
    total_expense = sum(t.amount for t in transactions if t.t_type == "Expense")
    remaining_balance = total_income - total_expense

    print("\n    - Summary -")
    print(f"    Total Income   : ${total_income:.2f}")
    print(f"    Total Expenses : ${total_expense:.2f}")
    print(f"    Current Remaining Balance: ${remaining_balance:.2f}")

    # Prepare list of categories with totals, last entry, remaining, etc.
    category_totals = []
    for cat, limit in budget_limits.items():
        spent = sum(t.amount for t in transactions if t.t_type == "Expense" and t.category == cat)
        expenses_in_cat = [t.date for t in transactions if t.t_type == "Expense" and t.category == cat]
        last_time = max(expenses_in_cat) if expenses_in_cat else "N/A"
        remaining = limit - spent
        category_totals.append((cat, spent, limit, remaining, last_time))

    # Sort categories by total spent descending
    category_totals.sort(key=lambda x: x[1], reverse=True)

    # Show % of total expenses per category
    print("\n    - Top Expense Distribution by Category -")
    for cat, spent, _, _, _ in category_totals:
        percent = (spent / total_expense * 100) if total_expense else 0
        print(f"    {cat:<15}| {percent:>5.1f}% of total expenses")

    # Detailed transactions
    print("\n    - Income Transactions -")
    found_income = False
    for item in transactions:
        if item.t_type == "Income":
            print(f"    {item.display_info()}")
            found_income = True
    if not found_income:
        print("    No income recorded yet.")

    print("\n    - Expense Transactions -")
    found_expense = False
    for item in transactions:
        if item.t_type == "Expense":
            print(f"    {item.display_info()}")
            found_expense = True
    if not found_expense:
        print("    No expenses recorded yet.")

    # ----- Total Budget Utilization -----
    total_budget = sum(budget_limits.values())

    if total_budget > 0:
        utilization = (total_expense / total_budget) * 100
        print(f"\n    Total Budget Planned : ${total_budget:.2f}")
        print(f"    Budget Utilization   : {utilization:.1f}%")

        if utilization > 100:
            print("    Status: You exceeded your overall budget!")
        elif utilization >= 90:
            print("    Status: You are very close to your total budget limit.")
        else:
            print("    Status: You are within your overall budget.")
    else:
        print("    No budgets have been set yet.")

    

    print("\n    ----------------------------")
    input("\n    Press the Enter key to continue...")
        
# Displaying the Main Menu and calling the functions based on what the user enters.
def main():
    # Initialize main data structures. Starting at 0 as a placeholder.
    transactions = []
    budget_limits = {"Food":0, "Transportation":0, "Entertainment":0, "Bills":0, "Other":0}

    # Load previously saved data
    load_data(transactions, budget_limits)
    
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
            add_income(transactions, budget_limits)
            
        elif option == "2":
            add_expense(transactions, budget_limits)
            
        elif option == "3":
            view_transactions(transactions)
            
        elif option == "4":
            setting_budget(budget_limits, transactions)
            
        elif option == "5":
            view_budget_summary(budget_limits, transactions)
            
        elif option == "6":
            generate_report(transactions, budget_limits)
            
        # If the user inputs 7, the loop will stop and end the program.
        elif option == "7":
            save_data(transactions, budget_limits)
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