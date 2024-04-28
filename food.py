import sqlite3
from tkinter import Tk, Label, Button, Entry, Listbox, Scrollbar, MULTIPLE, END
from datetime import datetime

def create_tables():
    conn = sqlite3.connect('meals.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS foods
                 (id INTEGER PRIMARY KEY, name TEXT, portion_size INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS food_logs
                 (id INTEGER PRIMARY KEY, person_name TEXT, food_id INTEGER, date TEXT,
                 FOREIGN KEY(food_id) REFERENCES foods(id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS all_foods
                 (id INTEGER PRIMARY KEY, person_name TEXT, food_name TEXT, date TEXT)''')
    # Pre-defined food items with portion sizes
    food_items = {
        "Chicken": 200,
        "Beef": 300,
        "Turkey": 180,
        "Rice": 400,
        "Bread": 100,
        "Pasta": 180,
        "Milk": 120,
        "Eggs": 70,
        "Muffins": 150,
        "Carrots": 50,
        "Spinach": 10,
        "Broccoli": 20,
        "Cheese": 110,
        "Cauliflower": 25,
        "Tomatoes": 30,
        "Beans": 100
    }
    for food, portion_size in food_items.items():
        c.execute("INSERT INTO foods (name, portion_size) VALUES (?, ?)", (food, portion_size))
    conn.commit()
    conn.close()

def insert_food():
    person_name = person_entry.get().strip()
    selected_foods = [food_listbox.get(idx) for idx in food_listbox.curselection()]
    if person_name and selected_foods:
        conn = sqlite3.connect('meals.db')
        c = conn.cursor()
        date = datetime.now().strftime('%Y-%m-%d')
        for food_name in selected_foods:
            # Check if the food already exists in the database
            c.execute("SELECT id FROM foods WHERE name=?", (food_name,))
            result = c.fetchone()
            if result:
                food_id = result[0]
            else:
                c.execute("INSERT INTO foods (name) VALUES (?)", (food_name,))
                conn.commit()
                food_id = c.lastrowid
            # Insert into food_logs table
            c.execute("INSERT INTO food_logs (person_name, food_id, date) VALUES (?, ?, ?)", (person_name, food_id, date))
            # Insert into all_foods table
            c.execute("INSERT INTO all_foods (person_name, food_name, date) VALUES (?, ?, ?)", (person_name, food_name, date))
            conn.commit()
        conn.close()
        status_label.config(text="Foods logged successfully for {}!".format(person_name))
    else:
        status_label.config(text="Please enter person name and select foods!")

def close_app():
    root.destroy()

# GUI setup
root = Tk()
root.title("Food Logger")

create_tables()  # Create tables if they don't exist

instructions_label = Label(root, text="Instructions:\n1. Enter your name.\n2. Select the foods you ate.\n3. Click 'Log Food' to save your selection.")
instructions_label.pack()

person_label = Label(root, text="Enter Your Name:")
person_label.pack()

person_entry = Entry(root, width=30)
person_entry.pack()

food_label = Label(root, text="Select Foods:")
food_label.pack()

food_listbox = Listbox(root, selectmode=MULTIPLE, height=10, width=30)
food_listbox.pack(side="left", fill="both", expand=True)

scrollbar = Scrollbar(root, orient="vertical", command=food_listbox.yview)
scrollbar.pack(side="right", fill="y")

food_listbox.config(yscrollcommand=scrollbar.set)

# Fetch pre-defined food items from the database
conn = sqlite3.connect('meals.db')
c = conn.cursor()
c.execute("SELECT name FROM foods")
food_items = [row[0] for row in c.fetchall()]
conn.close()

for food in food_items:
    food_listbox.insert(END, food)

log_button = Button(root, text="Log Food", command=insert_food)
log_button.pack()

status_label = Label(root, text="")
status_label.pack()

close_button = Button(root, text="Close", command=close_app)
close_button.pack()

root.mainloop()
