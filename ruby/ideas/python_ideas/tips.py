import tkinter as tk
from tkinter import messagebox

def calculate_tip_and_split():
    try:
        total_bill = float(total_bill_entry.get())
        num_people = int(num_people_entry.get())
        tip_percentage = float(tip_percentage_entry.get())

        # Calculate the tip amount
        tip_amount = total_bill * (tip_percentage / 100)
        
        # Calculate the total bill including tip
        total_with_tip = total_bill + tip_amount
        
        # Calculate the amount each person needs to pay
        amount_per_person = total_with_tip / num_people

        # Display the results
        total_with_tip_label.config(text=f"Total bill amount including {tip_percentage}% tip: ${total_with_tip:.2f}")
        amount_per_person_label.config(text=f"Each person needs to pay: ${amount_per_person:.2f}")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers.")

# Create the main window
root = tk.Tk()
root.title("Tip Splitting Calculator")

# Create labels and entry widgets
total_bill_label = tk.Label(root, text="Total Bill Amount:")
total_bill_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")

total_bill_entry = tk.Entry(root)
total_bill_entry.grid(row=0, column=1, padx=10, pady=5)

num_people_label = tk.Label(root, text="Number of People:")
num_people_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")

num_people_entry = tk.Entry(root)
num_people_entry.grid(row=1, column=1, padx=10, pady=5)

tip_percentage_label = tk.Label(root, text="Tip Percentage:")
tip_percentage_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")

tip_percentage_entry = tk.Entry(root)
tip_percentage_entry.grid(row=2, column=1, padx=10, pady=5)

calculate_button = tk.Button(root, text="Calculate", command=calculate_tip_and_split)
calculate_button.grid(row=3, column=0, columnspan=2, pady=10)

# Create labels to display results
total_with_tip_label = tk.Label(root, text="")
total_with_tip_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

amount_per_person_label = tk.Label(root, text="")
amount_per_person_label.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

# Start the GUI event loop
root.mainloop()
