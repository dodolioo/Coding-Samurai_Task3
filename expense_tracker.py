import tkinter as tk
from tkinter import messagebox, ttk
import datetime
import csv
import os

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")

        self.expenses = []
        self.load_data()

        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Amount:").grid(row=0, column=0, padx=5, pady=5)
        self.amount_entry = tk.Entry(frame)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Category:").grid(row=1, column=0, padx=5, pady=5)
        self.category_entry = tk.Entry(frame)
        self.category_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Description:").grid(row=2, column=0, padx=5, pady=5)
        self.description_entry = tk.Entry(frame)
        self.description_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(frame, text="Add Expense", command=self.add_expense).grid(row=3, column=0, columnspan=2, pady=10)

        self.tree = ttk.Treeview(self.root, columns=("date", "amount", "category", "description"), show='headings')
        self.tree.heading("date", text="Date")
        self.tree.heading("amount", text="Amount")
        self.tree.heading("category", text="Category")
        self.tree.heading("description", text="Description")
        self.tree.pack(pady=20)

        tk.Button(self.root, text="Generate Monthly Report", command=self.generate_report).pack(pady=10)

        self.update_treeview()

    def add_expense(self):
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        description = self.description_entry.get()
        date = datetime.date.today().strftime("%Y-%m-%d")

        if not amount or not category or not description:
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showwarning("Input Error", "Amount must be a number.")
            return

        self.expenses.append({"date": date, "amount": amount, "category": category, "description": description})
        self.save_data()
        self.update_treeview()

        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)

    def update_treeview(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for expense in self.expenses:
            self.tree.insert("", tk.END, values=(expense["date"], expense["amount"], expense["category"], expense["description"]))

    def generate_report(self):
        monthly_expenses = {}
        for expense in self.expenses:
            month = expense["date"][:7]
            if month not in monthly_expenses:
                monthly_expenses[month] = {}
            if expense["category"] not in monthly_expenses[month]:
                monthly_expenses[month][expense["category"]] = 0
            monthly_expenses[month][expense["category"]] += expense["amount"]

        report = ""
        for month, categories in monthly_expenses.items():
            report += f"Month: {month}\n"
            for category, amount in categories.items():
                report += f"  {category}: {amount}\n"

        messagebox.showinfo("Monthly Report", report)

    def save_data(self):
        with open("expenses.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["date", "amount", "category", "description"])
            for expense in self.expenses:
                writer.writerow([expense["date"], expense["amount"], expense["category"], expense["description"]])

    def load_data(self):
        if os.path.exists("expenses.csv"):
            with open("expenses.csv", newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    row["amount"] = float(row["amount"])
                    self.expenses.append(row)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
