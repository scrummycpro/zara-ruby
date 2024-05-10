import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import sqlite3

class DatabaseTransformerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Database Transformer")
        self.root.geometry("400x600")
        self.root.configure(background="black")

        # Create custom style
        self.style = ttk.Style()
        self.style.configure("Purple.TLabel", background="purple", foreground="white")
        self.style.configure("Lavender.TButton", background="#9370DB", foreground="white", padding=5)

        self.project_name_label = ttk.Label(self.root, text="Project Name:", style="Purple.TLabel")
        self.project_name_label.pack(pady=5)
        self.project_name_entry = ttk.Entry(self.root, style="Lavender.TEntry")
        self.project_name_entry.pack(pady=5)

        self.description_label = ttk.Label(self.root, text="Description:", style="Purple.TLabel")
        self.description_label.pack(pady=5)
        self.description_entry = ttk.Entry(self.root, style="Lavender.TEntry")
        self.description_entry.pack(pady=5)

        self.deliverable_label = ttk.Label(self.root, text="Deliverable:", style="Purple.TLabel")
        self.deliverable_label.pack(pady=5)
        self.deliverable_entry = ttk.Entry(self.root, style="Lavender.TEntry")
        self.deliverable_entry.pack(pady=5)

        self.money_owed_label = ttk.Label(self.root, text="Money Owed (Range):", style="Purple.TLabel")
        self.money_owed_label.pack(pady=5)
        self.money_owed_entry = ttk.Entry(self.root, style="Lavender.TEntry")
        self.money_owed_entry.pack(pady=5)

        self.date_started_label = ttk.Label(self.root, text="Date Started:", style="Purple.TLabel")
        self.date_started_label.pack(pady=5)
        self.date_started_entry = DateEntry(self.root, background='darkblue', foreground='white', borderwidth=2)
        self.date_started_entry.pack(pady=5)

        self.date_ended_label = ttk.Label(self.root, text="Date Ended:", style="Purple.TLabel")
        self.date_ended_label.pack(pady=5)
        self.date_ended_entry = DateEntry(self.root, background='darkblue', foreground='white', borderwidth=2)
        self.date_ended_entry.pack(pady=5)

        self.submit_button = ttk.Button(self.root, text="Submit", command=self.submit, style="Lavender.TButton")
        self.submit_button.pack(pady=5, fill='x')

        self.close_button = ttk.Button(self.root, text="Close", command=self.close_app, style="Lavender.TButton")
        self.close_button.pack(pady=5, fill='x')

    def submit(self):
        project_name = self.project_name_entry.get()
        description = self.description_entry.get()
        deliverable = self.deliverable_entry.get()
        money_owed = self.money_owed_entry.get()
        date_started = self.date_started_entry.get()
        date_ended = self.date_ended_entry.get()

        # Save data to the database file
        db_file = "money.db"  # Change this to your desired database file
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS projects
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     project_name TEXT,
                     description TEXT,
                     deliverable TEXT,
                     money_owed_range TEXT,
                     date_started TEXT,
                     date_ended TEXT)''')
        c.execute("INSERT INTO projects (project_name, description, deliverable, money_owed_range, date_started, date_ended) VALUES (?, ?, ?, ?, ?, ?)",
                   (project_name, description, deliverable, money_owed, date_started, date_ended))
        conn.commit()
        conn.close()

        # Show notification
        notification_message = f"Data successfully submitted to {db_file}"
        messagebox.showinfo("Notification", notification_message)

    def close_app(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseTransformerApp(root)
    root.mainloop()
