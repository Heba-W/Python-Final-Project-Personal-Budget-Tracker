# README PERSONAL_BUDGET_CALCULATOR_HKZ
Personal_Budget_Tracker.py is a high level application built and designed using the programming language know as "Python."
Developed with Jupyter notebook support, the structure and logic of the code are organized into modular sections to improve readability, efficiency, and testing.
This program uses proper naming conventions for variables and fuctions, this makes the code more understandable
for every person who decides to make use of the code and all of its resources.
In the main menu design, there are options for setting budget limits, adding income and adding expenses.
Expenses are what you spend your money on and in this program, the expenses are subtracted from the budget you set,
this helps youn  keep track of how much you should allow yourself to spend for each expense category.
The expense categories are food, transportation, entertainment, bills and others (which may include personal purchases or software purchases). After all the calculations and inputs from income, expenses and budgets are verified, there are options to view all transactions as well as receive a monthly report or summary. This allows you to analyze your spendings, salary and take note of any budget changes that you wish to consider.
The final report provides a complete financial breakdown of budget utilization, income and expense totals in addition to the long term tracking it offers to users. This program also possesses data persistence, ensuring that information is saved to non-volatile storage so that it remains available after the program terminates. All data is saved to a text file named budget_data.txt. When the program restarts, previously saved transactions and budgets are automatically loaded.

Further Breakdown of this Program:
The program allows users to add income by entering a description and an amount. The system validates the input to make sure the amount is numeric and at least one dollar. Once added, the income is stored as a Transaction object, saved to the file, and the program immediately recalculates and displays the current balance.

Expenses can also be added under predefined categories such as Food, Transportation, Entertainment, Bills, and Other. After selecting a category, the user enters a description and amount. The program validates the input to ensure the amount is positive. Once recorded, the expense is saved and the program checks whether the spending in that category is approaching or exceeding the set monthly budget. If spending reaches ninety percent of the budget, a caution message is displayed. If it exceeds the budget, a clear warning is shown. This feature helps users stay aware of their spending habits in real time.

Users can set monthly budgets for each expense category through a dedicated menu option. The system allows budgets to be zero or greater and saves changes immediately. These budget limits are later used to calculate remaining funds and generate summaries. The budget summary feature provides a detailed breakdown of income, expenses by category, remaining balances, and the date of the most recent transaction in each category. It also highlights categories that are close to or over budget.

The program also includes a report generation feature that produces a comprehensive financial overview. This report displays total income, total expenses, remaining balance, and overall budget utilization as a percentage. It also ranks categories by highest spending and shows how much each category contributes to total expenses. Finally, it lists all transactions in detail, giving the user a complete financial snapshot for the month.

The application runs through a menu driven interface that continuously prompts the user to choose an option. The menu includes adding income, adding expenses, viewing transactions, setting budgets, viewing a budget summary, generating a report, and saving and exiting. The loop continues running until the user chooses to exit, at which point the program saves all data to ensure nothing is lost.

Error handling is built into the system to prevent crashes from invalid input. The program checks for non numeric values, invalid category selections, negative amounts, and potential file reading or writing errors. If an issue occurs, the user receives a clear message and can try again without the program stopping unexpectedly.

Overall, the Personal Budget Calculator demonstrates how programming concepts can be applied to real world financial management. Beyond being a functional budgeting tool, the project serves as a strong example of how to design and implement a complete software application that solves a practical everyday problem.



