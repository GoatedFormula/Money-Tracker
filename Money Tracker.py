import tkinter
from tkinter import ttk
import csv
import os
from datetime import datetime

root = tkinter.Tk()
root.title("Expense Tracker")
root.geometry("1050x600")
root.configure(bg="#f0f0f0")
root.minsize(850, 500)

filePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "transactions.csv")

# Main layout
mainFrame = tkinter.Frame(root, bg="#f0f0f0")
mainFrame.pack(fill="both", expand=True, padx=20, pady=20)

# Left panel
leftFrame = tkinter.Frame(mainFrame, bg="#f0f0f0", width=300)
leftFrame.pack(side="left", fill="y", padx=(0, 20))
leftFrame.pack_propagate(False)

entryLabel = tkinter.Label(leftFrame, text="New Entry", font=("Arial", 28, "bold"), bg="#f0f0f0")
entryLabel.pack(pady=20)

gainLabel = tkinter.Label(leftFrame, text="Gain (RM):", font=("Arial", 16), bg="#f0f0f0")
gainLabel.pack(anchor="w", pady=(10, 5))

gainTextbox = tkinter.Entry(leftFrame, font=("Arial", 16), width=22)
gainTextbox.pack()

spentLabel = tkinter.Label(leftFrame, text="Spent (RM):", font=("Arial", 16), bg="#f0f0f0")
spentLabel.pack(anchor="w", pady=(20, 5))

spentTextbox = tkinter.Entry(leftFrame, font=("Arial", 16), width=22)
spentTextbox.pack()

balanceLabel = tkinter.Label(leftFrame, text="Balance: RM 0.00", font=("Arial", 20, "bold"), bg="#f0f0f0")
balanceLabel.pack(pady=30)

statusLabel = tkinter.Label(leftFrame, text="", font=("Arial", 11), bg="#f0f0f0", wraplength=270)
statusLabel.pack(pady=5)

# Right panel
rightFrame = tkinter.Frame(mainFrame, bg="#f0f0f0")
rightFrame.pack(side="right", fill="both", expand=True)

historyLabel = tkinter.Label(rightFrame, text="Transaction History", font=("Arial", 24, "bold"), bg="#f0f0f0")
historyLabel.pack(anchor="w", pady=(15, 20))

# Transaction table
tableFrame = tkinter.Frame(rightFrame)
tableFrame.pack(fill="both", expand=True)

columns = ("Date", "Gain", "Spent", "Balance")

transactionTable = ttk.Treeview(tableFrame, columns=columns, show="headings")

transactionTable.heading("Date", text="Date")
transactionTable.heading("Gain", text="Gain (RM)")
transactionTable.heading("Spent", text="Spent (RM)")
transactionTable.heading("Balance", text="Balance (RM)")

transactionTable.column("Date", width=150, anchor="center")
transactionTable.column("Gain", width=100, anchor="center")
transactionTable.column("Spent", width=100, anchor="center")
transactionTable.column("Balance", width=120, anchor="center")

scrollbar = ttk.Scrollbar(tableFrame, orient="vertical", command=transactionTable.yview)
transactionTable.configure(yscrollcommand=scrollbar.set)

transactionTable.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


def getBalance():
    total = 0

    if os.path.exists(filePath):
        with open(filePath, "r", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                total += float(row["Gain"]) - float(row["Spent"])

    return total


def loadTransactions():
    if os.path.exists(filePath):
        with open(filePath, "r", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                transactionTable.insert("", "end", values=(
                    row["Date"],
                    row["Gain"],
                    row["Spent"],
                    row["Balance"]
                ))

    balanceLabel.config(text=f"Balance: RM {getBalance():.2f}")


def saveTransaction():
    try:
        gain = float(gainTextbox.get() or 0)
        spent = float(spentTextbox.get() or 0)

        if gain < 0 or spent < 0:
            statusLabel.config(text="Amounts cannot be negative!", fg="red")
            return

        if gain == 0 and spent == 0:
            statusLabel.config(text="Enter an amount!", fg="red")
            return

        oldBalance = getBalance()
        newBalance = oldBalance + gain - spent

        fileExists = os.path.exists(filePath)

        with open(filePath, "a", newline="") as file:
            writer = csv.writer(file)

            if not fileExists or os.path.getsize(filePath) == 0:
                writer.writerow(["Date", "Gain", "Spent", "Balance"])

            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            writer.writerow([
                date,
                f"{gain:.2f}",
                f"{spent:.2f}",
                f"{newBalance:.2f}"
            ])

        transactionTable.insert("", "end", values=(
            date,
            f"{gain:.2f}",
            f"{spent:.2f}",
            f"{newBalance:.2f}"
        ))

        transactionTable.yview_moveto(1)

        balanceLabel.config(text=f"Balance: RM {newBalance:.2f}")

        gainTextbox.delete(0, tkinter.END)
        spentTextbox.delete(0, tkinter.END)

        statusLabel.config(text="Transaction saved!", fg="green")

    except ValueError:
        statusLabel.config(text="Please enter valid numbers!", fg="red")


saveButton = tkinter.Button(
    leftFrame,
    text="Save Transaction",
    font=("Arial", 14, "bold"),
    command=saveTransaction,
    bg="#2563eb",
    fg="white",
    padx=10,
    pady=8
)
saveButton.pack(pady=10)

# Load previous records
loadTransactions()

# Center window
root.update_idletasks()

windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()

screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()

x = (screenWidth - windowWidth) // 2
y = (screenHeight - windowHeight) // 2

root.geometry(f"{max(1050, windowWidth)}x{max(600, windowHeight)}+{x}+{y}")

root.mainloop()
