# Python Final Project - Personal Budget Calculator

# Importing necessary modules.
import os
from datetime import datetime

# Transaction class, which represents one single financial record.
class Transaction:
    def __init__(self, t_type, category, description, amount):
        # Income or Expense
        self.t_type = t_type
        # "Food", "Bills", "Salary", etc.
        self.category = category
        self.description = description
        self.amount = amount
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Formatting the transaction to appear organized.
    def display_info(self):
        if self.t_type == "Income":
            return f"{self.date} | {self.description:<10} | ${self.amount:>8.2f}"
        return f"{self.date} | {self.category} | {self.description:<10} | ${self.amount:>8.2f}"

# Text file where all information is stored.
DATA_FILE = "data.txt"

# Saving all data, such as transactions and budget limits, to a text file.
def save_data(transactions, budget_limits):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            # Saving budget limits
            file.write("[BUDGET_LIMITS]\n")
            for category, limit in budget_limits.items():
                file.write(f"{category}|{limit}\n")
            
            # Saving all transactions (income and expense) to the text file.
            file.write("[TRANSACTIONS]\n")
            for t in transactions:
                file.write(f"{t.t_type}|{t.category}|{t.description}|{t.amount}|{t.date}\n")
    except OSError as e:
        print(f"    Error saving data: {e}")

# Reading from the file to recreate/restore the previous Transaction objects budget limits.
def load_data(transactions, budget_limits):
    # If a data file doesn't exist, create an empty one so persistence always exists.
    if not os.path.exists(DATA_FILE):
        save_data(transactions, budget_limits)
        return

    # Determining which section of the file is being read.
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
                    # Budget Limits are stored in dictionary as category: limit.
                    if section == "BUDGET_LIMITS":
                        category, limit = line.split("|")
                        budget_limits[category] = float(limit)
                    # Recreating the transaction objects
                    elif section == "TRANSACTIONS":
                        t_type, category, description, amount, date = line.split("|")
                        t = Transaction(t_type, category, description, float(amount))
                        # Restore original timestamp.
                        t.date = date
                        transactions.append(t)
                except ValueError:
                    # Skip corrupted lines.
                    continue
    except OSError as e:
        print(f"    Error loading data: {e}")

# Dictionary for mapping numbers to categories for user selection.
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
        if amount >= 1:
            # Create a new income transaction object and add it to the transactions list.
            new_income = Transaction("Income", "N/A", description, amount)
            transactions.append(new_income)
            print("    Income was added successfully!")
            # Calculate total income and total expenses from all recorded transactions.
            total_income = sum(t.amount for t in transactions if t.t_type == "Income")
            total_expense = sum(t.amount for t in transactions if t.t_type == "Expense")
            balance = total_income - total_expense
            print(f"    Current balance: ${balance:.2f}")
            # Save data to text file.
            save_data(transactions, budget_limits)
        else:
            print("    Error: Amount must be at least $1.00. Transaction cancelled.")      
    except ValueError:
        print("    Error: Please enter a valid number for the amount.")

    print("\n")
    input("    Press the Enter key to continue...")

# Function to add expense
def add_expense(transactions, budget_limits):
    print("\n    --- Add Expense ---")
    print("    Select a Category:")
    for key, value in expense_cat.items():
        print(f"    {key}. {value}")
    try:
        choice = int(input("\n    Enter a category (1-5): "))
        if choice in expense_cat:
            desc = input("    Enter expense description: ")
            amt = float(input("    Enter the amount: "))
            if amt > 0:
                # Create new expense transaction using the class.
                # Also adding it to the list, updating the remaining budget, and saving to file.
                new_expense = Transaction("Expense", expense_cat[choice], desc, amt)
                transactions.append(new_expense)
                print(f"\n    Successfully added expense of ${amt:.2f} to {expense_cat[choice]}!")
                category = expense_cat[choice]
                limit = budget_limits.get(category, 0)
                # Display the remaining budget if the user has balance remaining.
                if limit > 0:
                    total_spent = sum(t.amount for t in transactions if t.t_type == "Expense" and t.category == category)
                    remaining = limit - total_spent
                    print(f"    Remaining {category} budget: ${remaining:.2f}")
                
                # Save data to text file.
                save_data(transactions, budget_limits)
                
                # Checking if the user is near or over the specific category budget and displaying warnings when needed.
                check_category_limit(expense_cat[choice], budget_limits, transactions)
            else:
                print("    Error: Amount must be positive.")
        else:
            print("    Error: Invalid category.")
    except ValueError:
        print("    Error: Please enter numbers only for category and amount.")
    
    input("\n    Press the Enter key to continue...")

# Function to check if user is near or over budget limit.
def check_category_limit(category, budget_limits, transactions):
    # Only check if the category has a budget (more than 0) set.
    if category in budget_limits and budget_limits[category] > 0:
        total_spent = sum(item.amount for item in transactions if item.t_type == "Expense" and item.category == category)
        
        limit = budget_limits[category]
        
        # Warning messages if total spent is greater than the set budget.
        if total_spent > limit:
            print(f"\n    !!! WARNING: You have exceeded your {category} budget by ${total_spent - limit:.2f} !!!")
        # Approaching limit, 90% or greater.
        elif total_spent >= limit * 0.9:
            print(f"\n    * Caution: You have used { (total_spent/limit)*100 :.1f}% of your {category} budget. *")
        # Informational message.
        else:
            print(f"\n    * You have used { (total_spent/limit)*100 :.1f}% of your {category} budget. *")

# Function to view all transactions
def view_transactions(transactions):
    print("\n    --- All Transactions ---")
    
    # Displaying all income transactions.
    print("\n    - Income Transactions -")
    # Checking if income transactions exist.
    found_income = False
    for item in transactions:
        if item.t_type == "Income":
            # Formatting info for each income transaction.
            print(f"    {item.display_info()}")
            found_income = True
    if not found_income:
        print("    No income recorded yet.")

    # Displaying all expense transactions.
    print("\n    - Expense Transactions -")
    # Checking if expense transactions exist
    found_expense = False
    for item in transactions:
        if item.t_type == "Expense":
            # Formatting info for each income transaction.
            print(f"    {item.display_info()}")
            found_expense = True
    if not found_expense:
        print("    No expenses recorded yet.")
        
    print("\n    -----------------------------")
    input("\n    Press the Enter key to continue...")

# Function to set a monthly budget for a specfic expense category.
def setting_budget(budget_limits, transactions):
    print("\n    --- Set Monthly Budget ---")
    # Showing list of categories for the user to choose from.
    for key, value in expense_cat.items():
        print(f"    {key}. {value}")
    try:
        choice = int(input("\n    Select a category to set a budget for (1-5): "))
        # Ask for a budget amount when the user enters a valid choice (category).
        if choice in expense_cat:
            category = expense_cat[choice]

            amount = float(input(f"    Enter the monthly budget for {category}: $"))
            
            # Update the budget_lists dictionary with the new amount.
            if amount > 0:
                budget_limits[category] = amount
                print(f"    Budget for {category} successfully set to ${amount:.2f}.")
                save_data(transactions, budget_limits)
                
            # If the user doesn't add a valid budget amount.
            else:
                print("    Error: Budget must be zero or greater.")
        else:
            print("    Error: Invalid category selection.")
    except ValueError:
        print("    Error: Please enter numeric values only.")
    input("\n    Press the Enter key to continue...")

# Function to view budget summary, including spending and remaining balance.
def view_budget_summary(budget_limits, transactions):
    print(f"\n    --- Budget Summary for This Month ---")
    # Displaying when summary was created.
    # strftime() allows formatting of how timestamp is displayed.
    print(f"    Summary generated at: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    
    # Calculate total income and total expenses based on all category transactions.
    total_income = sum(t.amount for t in transactions if t.t_type == "Income")
    total_expense = sum(t.amount for t in transactions if t.t_type == "Expense")
    current_balance = total_income - total_expense

    print(f"    INCOME:\n    Total Income: ${total_income:.2f}")
    print(f"\n    EXPENSES BY CATEGORY:\n")
    
    # Formatting as a table/chart
    print(f"    {'Category':<15} | {'Budget':<9} | {'Spent':<9} | {'Remaining':<10}")
    print("    ----------------------------------------------------------")
    
    # Preparing dictionaries to store the total spent and the last transaction date for each category.
    totals = {cat: 0 for cat in budget_limits}
    # Categories with no budget set appear as Not Applicable.
    last_entry = {cat: "N/A" for cat in budget_limits}
    
    # Calculating totals and tracking last transaction date.
    for item in transactions:
        if item.t_type == "Expense" and item.category in totals:
            totals[item.category] += item.amount
            # Update last entry timestamp for this category.
            last_entry[item.category] = item.date
    
    # Displaying each seperate category with budget, spent, remaining, and warning status.
    for cat, limit in budget_limits.items():
        spent = totals[cat]
        remaining = limit - spent
        status = ""
        if limit > 0:
            # Warn user if they are over budget.
            if spent > limit:  
                status = "  !! Warning: You are over budget !!"
            # If user is approaching the limit (around 90%).
            elif spent >= limit * 0.9:
                status = f" *Warning: 90% or more used.*"
        # Display info in chart/table format.
        print(f"    {cat:<15} | ${limit:>8.2f} | ${spent:>8.2f} | ${remaining:>9.2f} | {last_entry[cat]:<16} {status}")

    # Display totals and current balance remaining.
    print(f"\n    Total Expenses: ${total_expense:.2f}")
    print(f"    Current remaining Balance: ${current_balance:.2f}")
    input("\n    Press the Enter key to continue...")
    
# Function to generate a detailed monthly report
def generate_report(transactions, budget_limits):
    print("\n\n    --- Monthly Financial Report ---\n")
    print(f"    Report generated at: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # Calculating overall totals for income, expenses, and remaining balance.
    total_income = sum(t.amount for t in transactions if t.t_type == "Income")
    total_expense = sum(t.amount for t in transactions if t.t_type == "Expense")
    remaining_balance = total_income - total_expense

    # Displaying summary of totals
    print("\n    - Summary -")
    print(f"    Total Income   : ${total_income:.2f}")
    print(f"    Total Expenses : ${total_expense:.2f}")
    print(f"    Current Remaining Balance: ${remaining_balance:.2f}")

    # Prepare a list with category totals, last transaction date, and remaining budget for each category.
    category_totals = []
    for cat, limit in budget_limits.items():
        spent = sum(t.amount for t in transactions if t.t_type == "Expense" and t.category == cat)
        expenses_in_cat = [t.date for t in transactions if t.t_type == "Expense" and t.category == cat]
        # If category has no transaction, appear as Not Applicable.
        last_time = max(expenses_in_cat) if expenses_in_cat else "N/A"
        remaining = limit - spent
        # Adding to list.
        category_totals.append((cat, spent, limit, remaining, last_time))

    # Sort categories by total amount spent (descending order) to highlight the largest expenses.
    category_totals.sort(key=lambda x: x[1], reverse=True)

    # Show percentage of the user's total expenses per category.
    # (How much of their budget is going towards each category).
    print("\n    - Top Expense Distribution by Category -")
    for cat, spent, _, _, _ in category_totals:
        percent = (spent / total_expense * 100) if total_expense else 0
        print(f"    {cat:<15}| {percent:>5.1f}% of total expenses")

    # Show detailed income transactions.
    print("\n    - Income Transactions -")
    found_income = False
    for item in transactions:
        if item.t_type == "Income":
            print(f"    {item.display_info()}")
            found_income = True
    if not found_income:
        print("    No income recorded yet.")

    # Show detailed expense transactions.
    print("\n    - Expense Transactions -")
    found_expense = False
    for item in transactions:
        if item.t_type == "Expense":
            print(f"    {item.display_info()}")
            found_expense = True
    if not found_expense:
        print("    No expenses recorded yet.")

    # Calculating overall budget utilization.
    # Adding all budget amounts to get total.
    total_budget = sum(budget_limits.values())
    if total_budget > 0:
        # Multiplying by 100 to get the percent (out of 100).
        utilization = (total_expense / total_budget) * 100
        print(f"\n    Total Budget Planned : ${total_budget:.2f}")
        print(f"    Budget Utilization   : {utilization:.1f}%")

        # Displaying budget status depending on how much (percent) of the budget was used.
        if utilization > 100:
            print("    Status: Oh no! You exceeded your overall budget!")
        elif utilization >= 90:
            print("    Status: Be careful! You are very close to your total budget limit.")
        else:
            print("    Status: You are within your overall budget. Great!")
    else:
        print("    No budgets have been set yet.")

    print("\n    ----------------------------")
    input("\n    Press the Enter key to continue...")
        
# Main Program Function.
# Displays the menu and handles user interactions.
def main():
    # Initializing the data structures for transactions and budgets.
    transactions = []
    # Budgets start at 0 as a placeholder.
    budget_limits = {"Food":0, "Transportation":0, "Entertainment":0, "Bills":0, "Other":0}

    # Load previously saved data from file.
    load_data(transactions, budget_limits)
    
    # Main Menu Loop.
    # Repeatedly displays options until the user chooses to exit.
    while True:
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

        # Calling the appropriate function based on what the user enters.
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
        elif option == "7":
            # Saving all data to the text file and exiting the program.
            save_data(transactions, budget_limits)
            print("\n    Your information has been saved. Thanks for using the Personal Budget Tracker! Goodbye!")
            print("\n  ----------------------------------------------------")
            break
        else:
            # Handling invalid menu selections.
            print("\n    Invalid option. Please try again and enter a number between 1 and 7.")
            print("\n  ----------------------------------------------------")

# Run the program.
if __name__ == "__main__":
    main()