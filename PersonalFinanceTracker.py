# Import necessary modules
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from datetime import datetime

# Initializing global dictionary to store transactions
transactions = {}

# File handling functions
# Load transaction data from a JSON file
def load_transactions():
    global transactions
    try:
        with open('transactionsdictionary.json', 'r') as file:
            data = json.load(file)
            transactions = data.get('transactions', {})
    except (FileNotFoundError, json.JSONDecodeError):
        transactions = {}

# Save current transaction data to a JSON file
def save_transactions():
    with open('transactionsdictionary.json', 'w') as file:
        formatted_transactions = {'transactions': transactions}
        json.dump(formatted_transactions, file)

# Defining the functions of the main menu options
# Option - 6
# Open and read the file, then parse each line to add to the transactions dictionary
def read_bulk_transactions_from_file(filename):
    global transactions
    try:
        with open(filename, 'r') as file:
            for line in file:
                category, amount, transaction_type, date_str = line.strip().split(',')
                category = category.lower()
                date = datetime.strptime(date_str, '%Y-%m-%d')
                transactions.setdefault(category, [])
                transactions[category].append({'amount': float(amount), 'transaction_type': transaction_type, 'date': date.strftime('%Y-%m-%d')})
            save_transactions()
            print("Transaction added successfully!")
    except FileNotFoundError:
        print("Bulk transactions file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Option - 1
# Taking user inputs for transaction details and adds to the list
def add_transaction():
    print("Please enter the details according to the given format")
    category = input("Enter category: ").lower()
    while True:
        amount = input("Enter amount: ")
        try:
            amount = float(amount)
            break
        except ValueError:
            print("Invalid amount. Please enter a number.")
    while True:
        transaction_type = input("Enter transaction type (income/expense): ").lower()
        if transaction_type not in ("income", "expense"):
            print("Invalid transaction type. Please enter income or expense.")
        else:
            break
    while True:
        date_str = input("Enter date (YYYY-MM-DD): ")
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            break
        except ValueError:
            print("Invalid input. Please enter date in the valid format.")
    transactions.setdefault(category, [])
    transactions[category].append({'amount': amount, 'transaction_type': transaction_type, 'date': date.strftime('%Y-%m-%d')})
    save_transactions()
    print("Transaction added successfully!")

# Option - 2
# Display all available transactions
def view_transactions():
    if not transactions.items():
        print("No transactions found.")
        return
    for category, data in transactions.items():
        print(f"{category}:")
        for transaction in data:
            print(f"    | Amount: {transaction['amount']:.2f} | Transaction Type: {transaction['transaction_type']} | Date: {transaction['date']}")

# Option - 3
# Allows user to update an existing transaction
def update_transaction():
    if not transactions.items():
        print("No transactions found to update.")
        return
    view_transactions()
    while True:
        category = input("Enter category to update: ").lower()
        if category not in transactions:
            print("Invalid category. Please enter a category as shown above.")
        else:
            break
    index = int(input("Enter id of transaction to update (1,2,3,...): "))
    if 0 < index <= len(transactions[category]):
        entry = transactions[category][index - 1]
        amount, transaction_type, date_str = entry['amount'], entry['transaction_type'], entry['date']
        while True:
            new_amount = input("Enter the new amount: ") or amount
            try:
                new_amount = float(new_amount)
                break
            except ValueError:
                print("Invalid amount. Please enter a number.")
        while True:
            new_transaction_type = input("Enter transaction type to update (income/expense): ").lower()
            if new_transaction_type not in ("income", "expense"):
                print("Invalid transaction type. Please enter income or expense.")
            else:
                break
        while True:
            new_date_str = input("Enter new date (YYYY-MM-DD): ") or date_str
            try:
                new_date = datetime.strptime(new_date_str, '%Y-%m-%d')
                break
            except ValueError:
                print("Invalid date. Please enter the date in the correct format.")
        transactions[category][index - 1]['amount'] = new_amount
        transactions[category][index - 1]['transaction_type'] = new_transaction_type
        transactions[category][index - 1]['date'] = new_date.strftime('%Y-%m-%d')
        save_transactions()
        print("Transaction updated successfully.")
    else:
        print("Transaction not found. Check the transaction ID")

# Option - 4
# Delete an existing transaction
def delete_transaction():
    if not transactions.items():
        print("No transactions found to delete.")
        return
    view_transactions()
    while True:
        category = input("Enter category to delete: ").lower()
        if category not in transactions:
            print("Invalid category. Please enter a category as shown above.")
        else:
            break
    if not transactions[category]:
        del transactions[category]
        save_transactions()
        print("Transaction category deleted successfully!")
        return
    index = int(input("Enter id of transaction to delete (1,2,3,...): "))
    if category in transactions and 0 < index <= len(transactions[category]):
        del transactions[category][index - 1]
        save_transactions()
        print("Transaction deleted successfully!")
    else:
        print("Invalid transaction ID.")

# Option - 5
# Calculating the total expense
def display_summary():
    if not transactions.items():
        print("No transactions found to display summary.")
        return
    total_income = 0
    total_expense = 0
    balance = 0
    for category, data in transactions.items():
        for transaction in data:
            amount, transaction_type = transaction['amount'], transaction['transaction_type']
            if transaction_type == "income":
                total_income += amount
            else:
                total_expense += amount
    balance = total_income - total_expense
    print(f"Total Income: {total_income:.2f}")
    print(f"Total Expense: {total_expense:.2f}")
    print(f"Balance: {balance:.2f}")

# Option - 7
class FinanceTrackerGUI:
    def __init__(self, root, transactions):
        self.root = root
        self.transactions = transactions
        self.root.title("Personal Finance Tracker")
        self.menu_frame = None
        self.transactions_for_gui = self.convert_transactions_for_gui(transactions)
        self.create_widgets()
        self.display_transactions(self.transactions_for_gui)
        self.create_search_bar()

    def convert_transactions_for_gui(self, transactions_data):
        transactions_for_gui = []
        for category, transactions_list in transactions.items():
            for transaction in transactions_list:
                transaction_for_gui = {
                    "Category": category,
                    "Amount": transaction["amount"],
                    "Transaction Type": transaction["transaction_type"],
                    "Date": transaction["date"],
                }
                transactions_for_gui.append(transaction_for_gui)
        return transactions_for_gui

    def create_widgets(self):
        style = ttk.Style()
        style.configure("Blue.Treeview",
                        background="#87ceeb",
                        foreground="black",
                        fieldbackground="#f5f5f5",
                        font=("Helvetica", 10))

        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True)

        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(pady=10)

        reset_button = tk.Button(self.menu_frame, text="Reset", command=self.reset_transactions)
        reset_button.pack(side=tk.LEFT, padx=5)

        self.tree = ttk.Treeview(frame, columns=("Category", "Amount", "Transaction Type", "Date"), style="Blue.Treeview")
        self.tree.heading("#0", text="ID")
        self.tree.heading("Category", text="Category", command=lambda: self.sort_column("Category"))
        self.tree.heading("Amount", text="Amount", command=lambda: self.sort_column("Amount"))
        self.tree.heading("Transaction Type", text="Transaction Type", command=lambda: self.sort_column("Transaction Type"))
        self.tree.heading("Date", text="Date", command=lambda: self.sort_column("Date"))
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

    def create_search_bar(self):
        self.search_var = tk.StringVar()
        search_label = tk.Label(self.menu_frame, text="Search:")
        search_label.pack(side=tk.LEFT, padx=5)
        
        self.search_entry = tk.Entry(self.menu_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT)
        
        search_button = tk.Button(self.menu_frame, text="Search", command=self.search_transactions)
        search_button.pack(side=tk.LEFT, padx=5)        

    def load_transactions_tree(self, filename):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                return data.get("transactions", {})
        except FileNotFoundError:
            return {}
        
    def search_transactions(self):
            self.display_transactions(self.transactions_for_gui)
            search_term = self.search_var.get().lower()
            if not search_term:
                messagebox.showwarning("Empty Search", "Please enter a search term.")
                return
            
            filtered_transactions = []
            for transaction in self.transactions_for_gui:
                if (
                    search_term in transaction["Category"].lower()
                    or search_term in str(transaction["Amount"])
                    or search_term in transaction["Transaction Type"].lower()
                    or search_term in transaction["Date"]
                ):  
                    filtered_transactions.append(transaction)
            self.display_transactions(filtered_transactions)
            

    def sort_column(self, column):
        items = self.tree.get_children('')
        items = sorted(items, key=lambda x: self.tree.set(x, column))
        for index, item in enumerate(items):
            self.tree.move(item, '', index)

    def display_transactions(self, transactions):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for idx, transaction in enumerate(transactions, start=1):
            self.tree.insert("", "end", text=str(idx), values=(
                transaction['Category'],
                transaction['Amount'],
                transaction['Transaction Type'],
                transaction['Date']
                ))
        
    def display_all_transactions(self):
        self.display_transactions(self.transactions_for_gui)

    def reset_transactions(self):
        self.transactions = self.load_transactions_tree("transactionsdictionary.json")
        self.transactions_for_gui = self.convert_transactions_for_gui(self.transactions)
        self.display_all_transactions()

def launch_gui():
    root = tk.Tk()
    app = FinanceTrackerGUI(root, transactions)
    root.mainloop()

def main_menu():
    load_transactions()
    while True:
        print("\n=== Personal Finance Tracker ===")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Display Summary")
        print("6. Read Bulk Transactions From File")
        print("7. Launch GUI")
        print("8. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            add_transaction()
        elif choice == '2':
            view_transactions()
        elif choice == '3':
            update_transaction()
        elif choice == '4':
            delete_transaction()
        elif choice == '5':
            display_summary()
        elif choice == '6':
            filename = input("Enter the filename to load: ")
            read_bulk_transactions_from_file(filename)
        elif choice == '7':
            print("Launching GUI...")
            launch_gui()
        elif choice == '8':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")

if __name__ == "__main__":
    main_menu()
