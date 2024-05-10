import random
import tkinter as tk
import sqlite3

breakfast_foods = {
    "eggs": ["Omelette", "Scrambled Eggs", "Egg Sandwich", "Egg Salad"],
    "sausage": ["Sausage and Biscuits", "Sausage Breakfast Burrito", "Sausage Breakfast Casserole", "Sausage and Egg Muffins"],
    "bread": ["Biscuits and Gravy", "Biscuit Breakfast Sandwich", "Breakfast Tacos", "Breakfast Burrito", "Cornbread"],
}

lunch_foods = {
    "sandwich": ["Turkey Sandwich", "Grilled Cheese Sandwich", "Chicken Sandwich"],
    "hotdog": ["Plain Hot Dog", "Chili Cheese Dog", "Corn Dog", "Hot Dog with Sauerkraut"],
    "mac_and_cheese": ["Classic Mac and Cheese", "Baked Mac and Cheese", "Mac and Cheese with Bacon", "Mac and Cheese with Broccoli"],
    "pizza": ["Pepperoni Pizza", "Cheese Pizza", "Vegetable Pizza", "BBQ Chicken Pizza"],
    "bread": ["Garlic Bread", "French Bread", "Dinner Rolls", "Cornbread", "Banana Bread"],
}

dinner_foods = {
    "chicken": ["Grilled Chicken", "Chicken Stir-Fry", "Chicken Parmesan", "Baked Chicken"],
    "beef": ["Beef Stir-Fry", "Beef Stroganoff", "Beef Tacos", "Beef Curry"],
    "vegetarian": ["Vegetable Stir-Fry", "Stuffed Peppers", "Vegetarian Chili", "Eggplant Parmesan"],
    "bread": ["Garlic Bread", "French Bread", "Dinner Rolls", "Cornbread", "Banana Bread"],
}

def generate_menu():
    breakfast_menu = [random.choice(breakfast_foods[ingredient]) for ingredient in random.sample(breakfast_foods.keys(), 1)]
    lunch_menu = [random.choice(lunch_foods[ingredient]) for ingredient in random.sample(lunch_foods.keys(), 1)]
    dinner_menu = [random.choice(dinner_foods[ingredient]) for ingredient in random.sample(dinner_foods.keys(), 1)]
    return breakfast_menu, lunch_menu, dinner_menu

def save_menu_to_database(breakfast_menu, lunch_menu, dinner_menu):
    conn = sqlite3.connect("menus.db")
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS breakfast
                 (id INTEGER PRIMARY KEY, food TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS lunch
                 (id INTEGER PRIMARY KEY, food TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS dinner
                 (id INTEGER PRIMARY KEY, food TEXT)''')
    
    for food in breakfast_menu:
        c.execute("INSERT INTO breakfast (food) VALUES (?)", (food,))
    for food in lunch_menu:
        c.execute("INSERT INTO lunch (food) VALUES (?)", (food,))
    for food in dinner_menu:
        c.execute("INSERT INTO dinner (food) VALUES (?)", (food,))
    
    conn.commit()
    conn.close()

def generate_and_display_menu():
    breakfast_menu, lunch_menu, dinner_menu = generate_menu()

    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "Breakfast Menu:\n")
    for food in breakfast_menu:
        output_text.insert(tk.END, f"{food}\n")
    output_text.insert(tk.END, "\nLunch Menu:\n")
    for food in lunch_menu:
        output_text.insert(tk.END, f"{food}\n")
    output_text.insert(tk.END, "\nDinner Menu:\n")
    for food in dinner_menu:
        output_text.insert(tk.END, f"{food}\n")
    output_text.config(state=tk.DISABLED)
    
    save_menu_to_database(breakfast_menu, lunch_menu, dinner_menu)

# Create GUI window
root = tk.Tk()
root.title("Menu Generator")

# Create and place widgets
generate_button = tk.Button(root, text="Generate Menu", command=generate_and_display_menu)
generate_button.pack(pady=10)

output_text = tk.Text(root, height=15, width=50, state=tk.DISABLED)
output_text.pack()

# Run the GUI event loop
root.mainloop()
