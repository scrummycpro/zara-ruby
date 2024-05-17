import tkinter as tk
from tkinter import messagebox
import sqlite3

class TodoApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("To-Do List")
        
        self.conn = sqlite3.connect("todo.db")
        self.cursor = self.conn.cursor()
        self.create_table()
        
        self.tasks = []
        
        tk.Label(self.root, text="Task Name:").grid(row=0, column=0, padx=10, pady=10)
        self.task_entry = tk.Entry(self.root, width=40)
        self.task_entry.grid(row=0, column=1, padx=10, pady=10)
        
        self.add_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_button.grid(row=0, column=2, padx=5, pady=10)
        
        self.task_list = tk.Listbox(self.root, width=50)
        self.task_list.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        
        self.delete_button = tk.Button(self.root, text="Delete Task", command=self.delete_task)
        self.delete_button.grid(row=2, column=0, columnspan=3, padx=5, pady=10)

        self.load_tasks()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                                id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL
                            )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS deleted_tasks (
                                id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL
                            )''')
        self.conn.commit()

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.tasks.append(task)
            self.task_list.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)
            self.save_task(task)
        else:
            messagebox.showwarning("Warning", "Please enter a task.")

    def delete_task(self):
        try:
            selected_task_index = self.task_list.curselection()[0]
            task = self.task_list.get(selected_task_index)
            self.task_list.delete(selected_task_index)
            del self.tasks[selected_task_index]
            self.save_deleted_task(task)
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to delete.")

    def save_task(self, task):
        self.cursor.execute("INSERT INTO tasks (name) VALUES (?)", (task,))
        self.conn.commit()

    def save_deleted_task(self, task):
        self.cursor.execute("INSERT INTO deleted_tasks (name) VALUES (?)", (task,))
        self.conn.commit()

    def load_tasks(self):
        self.cursor.execute("SELECT name FROM tasks")
        rows = self.cursor.fetchall()
        for row in rows:
            self.task_list.insert(tk.END, row[0])
            self.tasks.append(row[0])

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TodoApp()
    app.run()
