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
        self.start_date_label = ttk.Label(self.root, text="Start Date:", style="Purple.TLabel")
        self.start_date_label.pack(pady=5)
        self.start_date_entry = DateEntry(self.root, background='blue', foreground='white')
        self.start_date_entry.pack(pady=5, padx=10, fill='x')

        # End Date Entry
        self.end_date_label = ttk.Label(self.root, text="End Date:", style="Purple.TLabel")
        self.end_date_label.pack(pady=5)
        self.end_date_entry = DateEntry(self.root, background='blue', foreground='white')
        self.end_date_entry.pack(pady=5, padx=10, fill='x')

        # Start Time Button
        self.start_time_button = ttk.Button(self.root, text="Start Time", command=self.select_start_time, style="Custom.TButton")
        self.start_time_button.pack(pady=5, fill='x')

        # End Time Button
        self.end_time_button = ttk.Button(self.root, text="End Time", command=self.select_end_time, style="Custom.TButton")
        self.end_time_button.pack(pady=5, fill='x')

        # Total Jobs Applied Today Entry
        self.total_jobs_label = ttk.Label(self.root, text="Total Jobs Applied Today:", style="Purple.TLabel")
        self.total_jobs_label.pack(pady=5)
        self.total_jobs_entry = ttk.Entry(self.root, state="normal", style="DarkBlue.TEntry")
        self.total_jobs_entry.pack(pady=5, padx=10, fill='x')

        # Submit Button
        self.submit_button = ttk.Button(self.root, text="Submit", command=self.submit, style="Custom.TButton")
        self.submit_button.pack(pady=5, fill='x')

        # Close Button
        self.close_button = ttk.Button(self.root, text="Close", command=self.close_app, style="Custom.TButton")
        self.close_button.pack(pady=5, fill='x')

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
        messagebox.showinfo("Notification", notification_message, icon="info", bg="blue")

    def close_app(self):
        confirm = messagebox.askyesno("Close Application", "Are you sure you want to close the application?")
        if confirm:
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseTransformerApp(root, "tasks.db")  # Change "tasks.db" to your desired database file name
    root.mainloop()
