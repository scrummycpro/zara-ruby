import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import sqlite3
import datetime

class DatabaseTransformerApp:
    def __init__(self, root, db_file):
        self.root = root
        self.root.title("Database Transformer")
        self.root.geometry("400x500")
        self.root.configure(background="white")
        self.db_file = db_file

        # Start Date Entry
        self.start_date_label = tk.Label(self.root, text="Start Date:", bg="white", fg="black")
        self.start_date_label.pack()
        self.start_date_entry = DateEntry(self.root, background='darkblue', foreground='white', borderwidth=2)
        self.start_date_entry.pack()

        # End Date Entry
        self.end_date_label = tk.Label(self.root, text="End Date:", bg="white", fg="black")
        self.end_date_label.pack()
        self.end_date_entry = DateEntry(self.root, background='darkblue', foreground='white', borderwidth=2)
        self.end_date_entry.pack()

        # Start Time Button
        self.start_time_button = tk.Button(self.root, text="Start Time", command=self.select_start_time)
        self.start_time_button.pack()

        # End Time Button
        self.end_time_button = tk.Button(self.root, text="End Time", command=self.select_end_time)
        self.end_time_button.pack()

        # Total Jobs Applied Today Entry
        self.total_jobs_label = tk.Label(self.root, text="Total Jobs Applied Today:", bg="white", fg="black")
        self.total_jobs_label.pack()
        self.total_jobs_entry = tk.Entry(self.root, state="normal")
        self.total_jobs_entry.pack()

        # Submit Button
        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit)
        self.submit_button.pack()

    def select_start_time(self):
        self.start_time_entry = self.get_current_time()
        messagebox.showinfo("Start Time", f"Start Time: {self.start_time_entry}")

    def select_end_time(self):
        self.end_time_entry = self.get_current_time()
        messagebox.showinfo("End Time", f"End Time: {self.end_time_entry}")

    def get_current_time(self):
        now = datetime.datetime.now()
        return now.strftime("%H:%M:%S")

    def calculate_total_jobs_today(self):
        today = datetime.date.today()
        today_str = today.strftime("%Y-%m-%d")
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM tasks WHERE start_date = ?", (today_str,))
        total_jobs_today = c.fetchone()[0]
        conn.close()
        return total_jobs_today

    def submit(self):
        # Save data to the database file
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        # Create the tasks table if it doesn't exist
        c.execute('''CREATE TABLE IF NOT EXISTS tasks
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     start_date TEXT,
                     start_time TEXT,
                     end_date TEXT,
                     end_time TEXT)''')

        # Insert data into the tasks table
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        c.execute("INSERT INTO tasks (start_date, start_time, end_date, end_time) VALUES (?, ?, ?, ?)",
                   (start_date, self.start_time_entry, end_date, self.end_time_entry))

        # Calculate total jobs applied today
        total_jobs_today = self.calculate_total_jobs_today()
        self.total_jobs_entry.config(state="normal")
        self.total_jobs_entry.delete(0, tk.END)
        self.total_jobs_entry.insert(0, str(total_jobs_today))
        self.total_jobs_entry.config(state="readonly")

        conn.commit()
        conn.close()

        # Show notification
        notification_message = "Data successfully submitted to the database."
        messagebox.showinfo("Notification", notification_message)

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseTransformerApp(root, "tasks.db")  # Change "tasks.db" to your desired database file name
    root.mainloop()
