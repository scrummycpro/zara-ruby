import sqlite3
from tkinter import Tk, Label, Button, Entry, Listbox, Scrollbar, MULTIPLE, END, Canvas, Frame
from datetime import datetime


def create_tables():
    conn = sqlite3.connect('meals.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS foods
                 (id INTEGER PRIMARY KEY, name TEXT, portion_size INTEGER, calories INTEGER, protein INTEGER, macros TEXT, micros TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS food_logs
                 (id INTEGER PRIMARY KEY, person_name TEXT, food_ids TEXT, date TEXT, total_calories INTEGER, total_protein INTEGER)''')

    food_items = {
        "Chicken": {"portion_size": 200, "calories": 335, "protein": 28, "macros": "Protein: 28g, Fat: 18g, Carbs: 0g", "micros": "Iron: 1.5mg, Vitamin B12: 0.3mcg"},
        "Beef": {"portion_size": 300, "calories": 600, "protein": 50, "macros": "Protein: 50g, Fat: 45g, Carbs: 0g", "micros": "Iron: 2.1mg, Vitamin B12: 2.8mcg"},
        "Turkey": {"portion_size": 180, "calories": 300, "protein": 35, "macros": "Protein: 35g, Fat: 15g, Carbs: 0g", "micros": "Iron: 1.2mg, Vitamin B12: 1.6mcg"},
        "Rice": {"portion_size": 400, "calories": 200, "protein": 4, "macros": "Protein: 4g, Fat: 0g, Carbs: 44g", "micros": "Iron: 0.6mg, Vitamin B6: 0.1mg"},
    }

    for food, details in food_items.items():
        c.execute("SELECT id FROM foods WHERE name=?", (food,))
        if not c.fetchone():
            c.execute("INSERT INTO foods (name, portion_size, calories, protein, macros, micros) VALUES (?, ?, ?, ?, ?, ?)",
                      (food, details["portion_size"], details["calories"], details["protein"], details["macros"], details["micros"]))

    conn.commit()
    conn.close()


def calculate_requirements(age):
    if age < 4:
        return 1000, 13
    elif age < 8:
        return 1400, 19
    elif age < 13:
        return 1800, 34
    elif age < 18:
        return 2200, 46
    elif age < 50:
        return 2500, 56
    else:
        return 2200, 60


def insert_food():
    person_name = person_entry.get().strip()
    try:
        age = int(age_entry.get().strip())
    except ValueError:
        status_label.config(text="Enter a valid age.")
        return

    selected_foods = [food_listbox.get(idx) for idx in food_listbox.curselection()]

    if person_name and selected_foods:
        conn = sqlite3.connect('meals.db')
        c = conn.cursor()
        date = datetime.now().strftime('%Y-%m-%d')
        total_calories = 0
        total_protein = 0
        food_ids = []

        calorie_req, protein_req = calculate_requirements(age)

        for food_name in selected_foods:
            c.execute("SELECT id, calories, protein FROM foods WHERE name=?", (food_name,))
            result = c.fetchone()
            if result:
                food_id, calories, protein = result
                food_ids.append(str(food_id))
                total_calories += calories
                total_protein += protein

        sugar_message = "✅ You're good on protein!" if total_protein >= protein_req else "⚠️ Add more protein-rich foods."

        c.execute("INSERT INTO food_logs (person_name, food_ids, date, total_calories, total_protein) VALUES (?, ?, ?, ?, ?)",
                  (person_name, ",".join(food_ids), date, total_calories, total_protein))

        conn.commit()
        conn.close()

        status_label.config(text=f"{person_name}, you logged {len(selected_foods)} food(s). Calories: {total_calories}, Protein: {total_protein}g\nNeed: {protein_req}g protein, {calorie_req} kcal\n{sugar_message}")
    else:
        status_label.config(text="Please enter your name, age, and select foods.")


def view_logs():
    log_window = Tk()
    log_window.title("📜 Past Food Logs")
    log_window.geometry("600x400")
    log_window.config(bg="#121A24")

    Label(log_window, text="🗂️ Logged Meals History", bg="#121A24", fg="#D6EAF8",
          font=("Arial", 16, "bold")).pack(pady=10)

    canvas = Canvas(log_window, bg="#121A24", highlightthickness=0)
    scroll_frame = Frame(canvas, bg="#121A24")
    scrollbar = Scrollbar(log_window, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((0, 0), window=scroll_frame, anchor='nw')

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    scroll_frame.bind("<Configure>", on_configure)

    conn = sqlite3.connect('meals.db')
    c = conn.cursor()
    c.execute('''SELECT fl.person_name, fl.date, fl.total_calories, fl.total_protein, fl.food_ids FROM food_logs fl ORDER BY fl.date DESC''')
    logs = c.fetchall()

    for log in logs:
        person_name, date, calories, protein, food_ids = log
        food_names = []
        for fid in food_ids.split(","):
            c.execute("SELECT name FROM foods WHERE id=?", (fid,))
            food = c.fetchone()
            if food:
                food_names.append(food[0])
        food_str = ", ".join(food_names)

        Label(scroll_frame,
              text=f"👤 {person_name} | 📅 {date}\n🍽️ Foods: {food_str}\n🔥 Calories: {calories} kcal | 💪 Protein: {protein}g",
              bg="#1A242F", fg="#D6EAF8", font=("Arial", 11),
              wraplength=550, justify="left", padx=10, pady=8).pack(pady=5, fill="x", padx=10)

    conn.close()


def close_app():
    root.destroy()

# GUI
root = Tk()
root.title("Meal Logger")
root.geometry("500x650")
root.config(bg="#121A24")

create_tables()

Label(root, text="🍽️ Food Logging System", bg="#121A24", fg="#D6EAF8", font=("Arial", 16, "bold")).pack(pady=15)
Label(root, text="Enter Your Name:", bg="#121A24", fg="#D6EAF8", font=("Arial", 12)).pack()
person_entry = Entry(root, width=30, font=("Arial", 12))
person_entry.pack(pady=5)

Label(root, text="Enter Your Age:", bg="#121A24", fg="#D6EAF8", font=("Arial", 12)).pack()
age_entry = Entry(root, width=30, font=("Arial", 12))
age_entry.pack(pady=5)

Label(root, text="Select Foods:", bg="#121A24", fg="#D6EAF8", font=("Arial", 12)).pack(pady=(15, 5))

food_listbox = Listbox(root, selectmode=MULTIPLE, height=8, width=30, font=("Arial", 12), bg="#1A242F", fg="#D6EAF8")
food_listbox.pack(padx=20)

scrollbar = Scrollbar(root, orient="vertical", command=food_listbox.yview)
scrollbar.place(in_=food_listbox, relx=1.0, rely=0, relheight=1.0, anchor='ne')
food_listbox.config(yscrollcommand=scrollbar.set)

conn = sqlite3.connect('meals.db')
c = conn.cursor()
c.execute("SELECT name FROM foods")
food_items = [row[0] for row in c.fetchall()]
conn.close()

for food in food_items:
    food_listbox.insert(END, food)

Button(root, text="Log Food", command=insert_food, bg="#D6EAF8", fg="#121A24", font=("Arial", 12, "bold")).pack(pady=15)
Button(root, text="View Logs", command=view_logs, bg="#D6EAF8", fg="#121A24", font=("Arial", 12, "bold")).pack(pady=5)
Button(root, text="Close", command=close_app, bg="#D6EAF8", fg="#121A24", font=("Arial", 12, "bold")).pack(pady=15)

status_label = Label(root, text="", bg="#121A24", fg="#D6EAF8", font=("Arial", 11, "italic"))
status_label.pack(pady=5)

root.mainloop()
