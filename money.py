import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import sqlite3

class DatabaseTransformerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Database Transformer")
        self.root.geometry("400x600")
        self.root.configure(background="white")

        self.project_name_label = tk.Label(self.root, text="Project Name:", bg="white", fg="black")
        self.project_name_label.pack()
        self.project_name_entry = tk.Entry(self.root)
        self.project_name_entry.pack()

        self.description_label = tk.Label(self.root, text="Description:", bg="white", fg="black")
        self.description_label.pack()
        self.description_entry = tk.Entry(self.root)
        self.description_entry.pack()

        self.deliverable_label = tk.Label(self.root, text="Deliverable:", bg="white", fg="black")
        self.deliverable_label.pack()
        self.deliverable_entry = tk.Entry(self.root)
        self.deliverable_entry.pack()

        self.money_owed_label = tk.Label(self.root, text="Money Owed (Range):", bg="white", fg="black")
        self.money_owed_label.pack()
        self.money_owed_entry = tk.Entry(self.root)
        self.money_owed_entry.pack()

        self.date_started_label = tk.Label(self.root, text="Date Started:", bg="white", fg="black")
        self.date_started_label.pack()
        self.date_started_entry = DateEntry(self.root, background='darkblue', foreground='white', borderwidth=2)
        self.date_started_entry.pack()

        self.date_ended_label = tk.Label(self.root, text="Date Ended:", bg="white", fg="black")
        self.date_ended_label.pack()
        self.date_ended_entry = DateEntry(self.root, background='darkblue', foreground='white', borderwidth=2)
        self.date_ended_entry.pack()

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit)
        self.submit_button.pack()

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

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseTransformerApp(root)
    root.mainloop()
