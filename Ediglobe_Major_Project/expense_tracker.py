import csv
from datetime import datetime
import matplotlib.pyplot as plt

FILE_NAME = "expenses.csv"

# LOAD EXPENSES FROM CSV FILE

def load_expenses():
    expenses = []

    try:
        with open(FILE_NAME, "r", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                expenses.append({
                    "amount": float(row["amount"]),
                    "category": row["category"],
                    "date": row["date"]
                })

    except FileNotFoundError:
        pass

    except (ValueError, KeyError):
        print("Warning: There was an error reading the expense file.")

    return expenses

# SAVE EXPENSES TO CSV FILE

def save_expenses(expenses):
    with open(FILE_NAME, "w", newline="") as file:
        fieldnames = ["amount", "category", "date"]

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for expense in expenses:
            writer.writerow(expense)

    print("\nExpenses saved successfully!")

# ADD AN EXPENSE

def add_expense(expenses):
    print("\n--- Add an Expense ---")

    while True:
        try:
            amount = float(input("Enter amount: "))

            if amount <= 0:
                print("Amount must be greater than 0.")
                continue

            break

        except ValueError:
            print("Invalid amount. Please enter a number.")

    category = input(
        "Enter category (Food/Transport/Entertainment/Other): "
    ).strip()

    while category == "":
        print("Category cannot be empty.")
        category = input("Enter category: ").strip()

    while True:
        date = input(
            "Enter date (YYYY-MM-DD), or press Enter for today's date: "
        ).strip()

        if date == "":
            date = datetime.now().strftime("%Y-%m-%d")
            break

        try:
            datetime.strptime(date, "%Y-%m-%d")
            break

        except ValueError:
            print("Invalid date. Please use YYYY-MM-DD.")

    expense = {
        "amount": amount,
        "category": category,
        "date": date
    }

    expenses.append(expense)

    print("\nExpense added successfully!")

# VIEW ALL EXPENSES
def view_expenses(expenses):
    print("\n--- All Expenses ---")

    if not expenses:
        print("No expenses recorded yet.")
        return

    print("-" * 55)
    print(f"{'No.':<5}{'Date':<15}{'Category':<20}{'Amount':>10}")
    print("-" * 55)

    for index, expense in enumerate(expenses, start=1):
        print(
            f"{index:<5}"
            f"{expense['date']:<15}"
            f"{expense['category']:<20}"
            f"{expense['amount']:>10.2f}"
        )

    print("-" * 55)

# GENERATE EXPENSE REPORT
def generate_report(expenses):
    print("\n--- Expense Report ---")

    if not expenses:
        print("No expenses available for the report.")
        return

    total = sum(expense["amount"] for expense in expenses)

    highest = max(expenses, key=lambda expense: expense["amount"])

    average = total / len(expenses)

    print(f"\nTotal Spending : {total:.2f}")
    print(f"Average Expense: {average:.2f}")
    print(
        f"Highest Expense: {highest['amount']:.2f} "
        f"({highest['category']} on {highest['date']})"
    )

    category_totals = {}

    for expense in expenses:
        category = expense["category"]

        if category not in category_totals:
            category_totals[category] = 0

        category_totals[category] += expense["amount"]

    print("\nCategory-wise Spending:")
    print("-" * 35)

    for category, amount in category_totals.items():
        print(f"{category:<20} {amount:>10.2f}")

    print("-" * 35)

# MONTHLY SPENDING REPORT
def monthly_report(expenses):
    print("\n--- Monthly Spending ---")

    if not expenses:
        print("No expenses available.")
        return

    monthly_totals = {}

    for expense in expenses:
        month = expense["date"][:7]

        if month not in monthly_totals:
            monthly_totals[month] = 0

        monthly_totals[month] += expense["amount"]

    print("\nMonth-wise Spending:")
    print("-" * 30)

    for month, amount in sorted(monthly_totals.items()):
        print(f"{month:<15} {amount:>10.2f}")

    print("-" * 30)

# VISUALIZE EXPENSES
def visualize_expenses(expenses):
    if not expenses:
        print("\nNo expenses available for visualization.")
        return

    category_totals = {}

    for expense in expenses:
        category = expense["category"]

        if category not in category_totals:
            category_totals[category] = 0

        category_totals[category] += expense["amount"]

    categories = list(category_totals.keys())
    amounts = list(category_totals.values())
    plt.figure(figsize=(8, 6))

    plt.pie(
        amounts,
        labels=categories,
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title("Expense Distribution by Category")

    plt.tight_layout()
    plt.show()

# MAIN MENU
def main():
    expenses = load_expenses()

    print("=" * 55)
    print("          WELCOME TO PERSONAL EXPENSE TRACKER")
    print("=" * 55)

    while True:
        print("\nMain Menu")
        print("-" * 30)
        print("1. Add an Expense")
        print("2. View All Expenses")
        print("3. Generate Report")
        print("4. Monthly Report")
        print("5. Visualize Expenses")
        print("6. Save and Exit")
        print("-" * 30)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_expense(expenses)

        elif choice == "2":
            view_expenses(expenses)

        elif choice == "3":
            generate_report(expenses)

        elif choice == "4":
            monthly_report(expenses)

        elif choice == "5":
            visualize_expenses(expenses)

        elif choice == "6":
            save_expenses(expenses)
            print("\nThank you for using Personal Expense Tracker!")
            break

        else:
            print("\nInvalid choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()