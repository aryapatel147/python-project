import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os


class ExpenseTracker:
    def __init__(self, filename="expenses.csv"):
        self.filename = filename

        if os.path.exists(self.filename):
            self.data = pd.read_csv(self.filename)
        else:
            self.data = pd.DataFrame(columns=["Date", "Amount", "Category", "Description"])
            self.data.to_csv(self.filename, index=False)

        self._clean_data()

    def _clean_data(self):
        if not self.data.empty:
            self.data["Date"] = pd.to_datetime(self.data["Date"], errors="coerce")
            self.data["Amount"] = pd.to_numeric(self.data["Amount"], errors="coerce")
            self.data["Category"] = self.data["Category"].astype(str).str.strip()
            self.data.dropna(inplace=True)

    def add_expense(self, date, amount, category, description):
        try:
            datetime.strptime(date, "%Y-%m-%d")

            if float(amount) <= 0:
                print("Amount must be positive.")
                return False

            new_row = {
                "Date": pd.to_datetime(date),
                "Amount": float(amount),
                "Category": category.strip(),
                "Description": description
            }

            self.data = pd.concat([self.data, pd.DataFrame([new_row])], ignore_index=True)
            self.data.to_csv(self.filename, index=False)
            print(" Expense added successfully")
            return True

        except ValueError:
            print("Invalid date format! Use YYYY-MM-DD")
            return False

    def get_summary(self):
        if self.data.empty:
            return "No data available."

        total = np.sum(self.data["Amount"])
        average = np.mean(self.data["Amount"])
        category_summary = self.data.groupby("Category")["Amount"].sum()

        return {
            "total": total,
            "average": average,
            "by_category": category_summary
        }

    def filter_expenses(self, start_date=None, end_date=None, categories=None, min_amount=None, max_amount=None):
        df = self.data.copy()

        # ama Convert category only AFTER cp che
        df["Category"] = df["Category"].astype(str).str.strip().str.lower()

        if start_date is not None:
            df = df[df["Date"] >= pd.to_datetime(start_date, errors="coerce")]

        if end_date is not None:
            df = df[df["Date"] <= pd.to_datetime(end_date, errors="coerce")]

        if categories is not None:
            categories = [c.strip().lower() for c in categories]
            df = df[df["Category"].isin(categories)]

        if min_amount:
            df = df[df["Amount"] >= min_amount]

        if max_amount:
            df = df[df["Amount"] <= max_amount]

        return df

    def generate_report(self):
        summary = self.get_summary()
        if isinstance(summary, str):
            return summary

        report = f"""
------------ EXPENSE REPORT ---------------
Total Spending: ₹{summary['total']:.2f}
Average Spending: ₹{summary['average']:.2f}

Category Breakdown:
{summary['by_category']}
-------------------------------------------
"""
        return report

    def plot_category_bar(self):
        if self.data.empty:
            print("No data for visualization.")
            return

        plt.figure(figsize=(8, 5))
        sns.barplot(x=self.data["Category"], y=self.data["Amount"], estimator=sum)
        plt.title("Total Expenses by Category")
        plt.xlabel("Category")
        plt.ylabel("Total Amount")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_time_series(self):
        if self.data.empty:
            print("No data for visualization.")
            return

        df = self.data.copy()
        df = df.groupby("Date")["Amount"].sum()

        plt.figure(figsize=(10, 5))
        plt.plot(df.index, df.values, marker='o')
        plt.title("Spending Trend Over Time")
        plt.xlabel("Date")
        plt.ylabel("Amount")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_pie_by_category(self):
        if self.data.empty:
            print("No data for visualization.")
            return

        plt.figure(figsize=(7, 7))
        self.data.groupby("Category")["Amount"].sum().plot.pie(autopct='%1.1f%%')
        plt.title("Spending Distribution by Category")
        plt.ylabel("")
        plt.show()

    def plot_histogram(self):
        if self.data.empty:
            print("No data for visualization.")
            return

        plt.figure(figsize=(8, 5))
        plt.hist(self.data["Amount"], bins=10)
        plt.title("Expense Amount Distribution")
        plt.xlabel("Amount")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.show()


def main():
    tracker = ExpenseTracker()

    while True:
        print("\n------------ Smart Expense Tracker-------------")
        print("1. Add Expense")
        print("2. View Summary")
        print("3. Filter Expenses")
        print("4. Generate Report")
        print("5. Visualizations")
        print("6. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            date = input("Enter date (YYYY-MM-DD): ")
            amount = input("Enter amount: ")
            category = input("Enter category: ")
            description = input("Enter description: ")
            tracker.add_expense(date, amount, category, description)

        elif choice == "2":
            print("\n--- Summary ---")
            summary = tracker.get_summary()
            print(summary)

        elif choice == "3":
            start = input("Start Date (YYYY-MM-DD or blank): ").strip()
            if start.lower() in ("", "blank"):
                start = None

            end = input("End Date (YYYY-MM-DD or blank): ").strip()
            if end.lower() in ("", "blank"):
                end = None

            cat = input("Categories comma-separated (blank for all): ").strip()
            cats = cat.split(",") if cat.lower() not in ("", "blank") else None

            filtered = tracker.filter_expenses(
                start_date=start,
                end_date=end,
                categories=cats
            )
            print(filtered)

        elif choice == "4":
            print(tracker.generate_report())

        elif choice == "5":
            print("1. Bar Chart")
            print("2. Line Chart")
            print("3. Pie Chart")
            print("4. Histogram")
            opt = input("Choose: ")

            if opt == "1":
                tracker.plot_category_bar()
            elif opt == "2":
                tracker.plot_time_series()
            elif opt == "3":
                tracker.plot_pie_by_category()
            elif opt == "4":
                tracker.plot_histogram()

        elif choice == "6":
            break

        else:
            print("Invalid choice, try again!")

if __name__ == "__main__":
    main()

    


        

