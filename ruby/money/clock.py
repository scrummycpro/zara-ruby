import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3
import datetime

class DatabaseTransformerApp:
    def __init__(self, root, db_file):
        self.root = root
        self.root.title("Database Transformer")
        self.root.geometry("400x500")
        self.root.configure(background="black")
        self.db_file = db_file

        # Create a custom style for 3D buttons
        self.style = ttk.Style()
        self.style.configure("Custom.TButton", relief="raised", background="#9370DB", foreground="white", padding=5)

        # Start Date Entry
        self.start_date_label = ttk.Label(self.root, text="Start Date:")
        self.start_date_label.pack(pady=5)
        self.start_date_entry = DateEntry(self.root, background='blue', foreground='white')
        self.start_date_entry.pack(pady=5, padx=10, fill='x')

        # End Date Entry
        self.end_date_label = ttk.Label(self.root, text="End Date:")
        self.end_date_label.pack(pady=5)
        self.end_date_entry = DateEntry(self.root, background='blue', foreground='white')
        self.end_date_entry.pack(pady=5, padx=10, fill='x')

        # Start Time Entry
        self.start_time_label = ttk.Label(self.root, text="Start Time:")
        self.start_time_label.pack(pady=5)
        self.start_time_entry = ttk.Entry(self.root)
        self.start_time_entry.pack(pady=5, padx=10, fill='x')

        # End Time Entry
        self.end_time_label = ttk.Label(self.root, text="End Time:")
        self.end_time_label.pack(pady=5)
        self.end_time_entry = ttk.Entry(self.root)
        self.end_time_entry.pack(pady=5, padx=10, fill='x')

        # Total Jobs Applied Entry
        self.total_jobs_label = ttk.Label(self.root, text="Total Jobs Applied:")
        self.total_jobs_label.pack(pady=5)
        self.total_jobs_entry = ttk.Entry(self.root)
        self.total_jobs_entry.pack(pady=5, padx=10, fill='x')

        # Notes Entry
        self.notes_label = ttk.Label(self.root, text="Notes:")
        self.notes_label.pack(pady=5)
        self.notes_entry = ttk.Entry(self.root)
        self.notes_entry.pack(pady=5, padx=10, fill='x')

        # Start Time Button
        self.start_time_button = ttk.Button(self.root, text="Select Start Time", command=self.select_start_time, style="Custom.TButton")
        self.start_time_button.pack(pady=5, fill='x')

        # End Time Button
        self.end_time_button = ttk.Button(self.root, text="Select End Time", command=self.select_end_time, style="Custom.TButton")
        self.end_time_button.pack(pady=5, fill='x')

        # Submit Button
        self.submit_button = ttk.Button(self.root, text="Submit", command=self.submit, style="Custom.TButton")
        self.submit_button.pack(pady=5, fill='x')

    def select_start_time(self):
        self.start_time_entry.delete(0, tk.END)  # Clear previous entry
        self.start_time_entry.insert(0, self.get_current_time())

    def select_end_time(self):
        self.end_time_entry.delete(0, tk.END)  # Clear previous entry
        self.end_time_entry.insert(0, self.get_current_time())

    def submit(self):
        # Save data to the database file
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        # Insert data into the tasks table
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        total_jobs = self.total_jobs_entry.get()
        notes = self.notes_entry.get()  # Retrieve notes from the entry
        c.execute("INSERT INTO tasks (start_date, start_time, end_date, end_time, total_jobs, notes) VALUES (?, ?, ?, ?, ?, ?)",
                   (start_date, self.start_time_entry.get(), end_date, self.end_time_entry.get(), total_jobs, notes))

        conn.commit()
        conn.close()

        # Show notification
        notification_message = "Data successfully submitted to the database."
        messagebox.showinfo("Notification", notification_message, icon="info", bg="blue")

    def get_current_time(self):
        now = datetime.datetime.now()
        return now.strftime("%H:%M:%S")

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseTransformerApp(root, "task.db")  # Change "tasks.db" to your desired database file name
    root.mainloop()
