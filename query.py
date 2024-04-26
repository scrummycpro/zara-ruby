import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class SQLiteQueryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SQLite Query Tool")
        self.root.geometry("600x400")
        self.root.configure(background="black")

        # Database file entry
        self.db_file_label = ttk.Label(self.root, text="Database File:", background="black", foreground="white")
        self.db_file_label.grid(row=0, column=0, padx=10, pady=5)
        self.db_file_entry = ttk.Entry(self.root)
        self.db_file_entry.grid(row=0, column=1, padx=10, pady=5)

        # Query entry
        self.query_label = ttk.Label(self.root, text="SQL Query:", background="black", foreground="white")
        self.query_label.grid(row=1, column=0, padx=10, pady=5)
        self.query_entry = ttk.Entry(self.root)
        self.query_entry.grid(row=1, column=1, padx=10, pady=5)
        self.query_entry.insert(0, "SELECT * FROM tasks")

        # Submit button
        self.submit_button = ttk.Button(self.root, text="Submit", command=self.submit_query, style="Lavender.TButton")
        self.submit_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Close button
        self.close_button = ttk.Button(self.root, text="Close", command=self.close_app, style="Lavender.TButton")
        self.close_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Results treeview
        self.results_tree = ttk.Treeview(self.root, columns=("Result"), style="Result.Treeview")
        self.results_tree.grid(row=3, column=0, columnspan=2, padx=10, pady=5)
        self.results_tree.heading("#0", text="Result")
        self.results_tree.tag_configure("oddrow", background="black", foreground="white")
        self.results_tree.tag_configure("evenrow", background="black", foreground="white")

        # Custom style for buttons and treeview
        self.style = ttk.Style()
        self.style.configure("Lavender.TButton", background="#9370DB", foreground="white", padding=5)
        self.style.configure("Result.Treeview", background="black", foreground="white")

    def submit_query(self):
        # Get database file and query from entry fields
        db_file = self.db_file_entry.get()
        query = self.query_entry.get()

        try:
            # Connect to the database and execute the query
            conn = sqlite3.connect(db_file)
            c = conn.cursor()
            c.execute(query)
            rows = c.fetchall()
            conn.close()

            # Clear previous results
            for row in self.results_tree.get_children():
                self.results_tree.delete(row)

            # Insert new results into treeview
            for i, row in enumerate(rows):
                tag = "oddrow" if i % 2 == 0 else "evenrow"
                self.results_tree.insert("", tk.END, text=row, tags=(tag,))
        
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def close_app(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SQLiteQueryApp(root)
    root.mainloop()
