
import tkinter
import csv
import os
from datetime import datetime

root = tkinter.Tk()
root.title("Expense Tracker")
root.configure(bg="#f0f0f0")

# Main container
mainFrame = tkinter.Frame(root, bg="#f0f0f0")
mainFrame.pack(padx=40, pady=30)

entryLabel = tkinter.Label(mainFrame, text="Expense Tracker", font=("Arial", 32, "bold"), bg="#f0f0f0")
entryLabel.pack(pady=20)

gainLabel = tkinter.Label(mainFrame, text="Gain:", font=("Arial", 18), bg="#f0f0f0")
gainLabel.pack(pady=(10, 5))

gainTextbox = tkinter.Entry(mainFrame, font=("Arial", 16), width=25, justify="center")
gainTextbox.pack()

spentLabel = tkinter.Label(mainFrame, text="Spent:", font=("Arial", 18), bg="#f0f0f0")
spentLabel.pack(pady=(20, 5))

spentTextbox = tkinter.Entry(mainFrame, font=("Arial", 16), width=25, justify="center")
spentTextbox.pack()

balanceLabel = tkinter.Label(mainFrame, text="Balance: RM 0.00", font=("Arial", 24, "bold"), bg="#f0f0f0")
balanceLabel.pack(pady=25)

statusLabel = tkinter.Label(mainFrame, text="", font=("Arial", 12), bg="#f0f0f0")
statusLabel.pack(pady=5)

filePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "transactions.csv")


def getBalance():
    total = 0

    if os.path.exists(filePath):
        with open(filePath, "r", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                total += float(row["Gain"]) - float(row["Spent"])

    return total


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

            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                gain,
                spent,
                newBalance
            ])

        balanceLabel.config(text=f"Balance: RM {newBalance:.2f}")

        gainTextbox.delete(0, tkinter.END)
        spentTextbox.delete(0, tkinter.END)

        statusLabel.config(text="Transaction saved successfully!", fg="green")

    except ValueError:
        statusLabel.config(text="Please enter valid numbers!", fg="red")


saveButton = tkinter.Button(mainFrame, text="Save Transaction", font=("Arial", 16), command=saveTransaction)
saveButton.pack(pady=10)

balanceLabel.config(text=f"Balance: RM {getBalance():.2f}")

# Automatically fit window to content and center it
root.update_idletasks()

windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()

screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()

x = (screenWidth - windowWidth) // 2
y = (screenHeight - windowHeight) // 2

root.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")

root.mainloop()
