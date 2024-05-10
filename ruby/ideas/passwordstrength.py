import tkinter as tk
from tkinter import messagebox

class PasswordStrengthChecker:
    def __init__(self, master):
        self.master = master
        master.title("Password Strength Checker")
        master.geometry("300x150")
        master.configure(background='black')

        self.password_label = tk.Label(master, text="Enter Password:", bg='black', fg='white')
        self.password_label.pack(pady=5)

        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.pack(pady=5)

        self.check_button = tk.Button(master, text="Check", command=self.check_password, bg='rosy brown')
        self.check_button.pack(pady=5)

    def check_password(self):
        password = self.password_entry.get()

        if len(password) < 6:
            messagebox.showwarning("Weak Password", "Password is too short. Please use at least 6 characters.")
        elif len(password) < 10:
            messagebox.showinfo("Medium Password", "Password strength: Medium")
        else:
            messagebox.showinfo("Strong Password", "Password strength: Strong")

def main():
    root = tk.Tk()
    app = PasswordStrengthChecker(root)
    root.mainloop()

if __name__ == "__main__":
    main()
