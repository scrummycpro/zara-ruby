import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class WorkoutLogger(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Workout Logger")
        self.geometry("450x300")
        self.configure(bg='#2E3440')
        self.style = ttk.Style(self)
        self.setup_styles()
        self.create_widgets()
        self.calories_burned = 0
        self.create_database()

    def setup_styles(self):
        self.style.theme_use('clam')
        self.style.configure('.', background='#2E3440', foreground='#D8DEE9', fieldbackground='#3B4252')
        self.style.map('TCombobox', fieldbackground=[('readonly', '#3B4252')])
        self.style.configure('TButton', background='#B5E48C', foreground='#2E3440', font=('Helvetica', 10, 'bold'))
        self.style.configure('TLabel', background='#2E3440', foreground='#D8DEE9', font=('Helvetica', 10))
        self.style.configure('TEntry', background='#3B4252', foreground='#ECEFF4')
        self.style.configure('TFrame', background='#2E3440')
        self.style.configure('TScrollbar', background='#3B4252', troughcolor='#3B4252')

    def create_widgets(self):
        # Main frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(pady=10, padx=10)

        # Name selection
        self.name_label = ttk.Label(self.main_frame, text="Select Your Name:")
        self.name_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        names = ["Nicholas", "Samantha", "Zara", "Jasmine", "Aria"]
        self.name_var = tk.StringVar(value=names[0])
        self.name_menu = ttk.Combobox(self.main_frame, textvariable=self.name_var, values=names, width=18, state='readonly')
        self.name_menu.grid(row=0, column=1, padx=5, pady=5)

        # Exercise selection
        self.exercise_label = ttk.Label(self.main_frame, text="Select Exercise:")
        self.exercise_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')

        # Updated exercise list
        exercises = self.get_exercise_list()
        self.exercise_var = tk.StringVar(value=exercises[0])
        self.exercise_menu = ttk.Combobox(self.main_frame, textvariable=self.exercise_var, values=exercises, width=18, state='readonly')
        self.exercise_menu.grid(row=1, column=1, padx=5, pady=5)

        # Add custom exercise
        self.add_exercise_button = ttk.Button(self.main_frame, text="Add Exercise", command=self.add_exercise)
        self.add_exercise_button.grid(row=1, column=2, padx=5, pady=5)

        # Duration or reps input
        self.detail_label = ttk.Label(self.main_frame, text="Enter Reps/Duration(min)/Miles:")
        self.detail_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.detail_entry = ttk.Entry(self.main_frame)
        self.detail_entry.grid(row=2, column=1, padx=5, pady=5)

        # Log button
        self.log_button = ttk.Button(self.main_frame, text="Log Exercise", command=self.log_exercise)
        self.log_button.grid(row=2, column=2, padx=5, pady=5)

        # Total calories and protein
        self.total_label = ttk.Label(self.main_frame, text="Total Calories Burned: 0 kcal")
        self.total_label.grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.protein_label = ttk.Label(self.main_frame, text="Recommended Protein Intake: 0 g")
        self.protein_label.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        # Adding padding to all widgets
        for child in self.main_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def get_exercise_list(self):
        # Updated exercise list with categories: Calisthenics, Cardio, Weight Lifting
        exercises = [
            # Calisthenics
            "Push-ups", "Pull-ups", "Squats", "Lunges", "Planks",
            "Burpees", "Mountain Climbers", "Jumping Jacks", "Sit-ups", "Crunches",

            # Cardio
            "Running", "Walking", "Biking", "Jump Rope", "Stair Climbing",
            "Elliptical", "Rowing", "Swimming", "Aerobics", "HIIT",

            # Weight Lifting
            "Bench Press", "Deadlift", "Squat (Weighted)", "Overhead Press", "Bicep Curls",
            "Tricep Extensions", "Leg Press", "Lat Pulldowns", "Shoulder Press", "Dumbbell Rows",

            # Other
            "Yoga", "Pilates", "Stretching", "Other"
        ]
        return exercises

    def add_exercise(self):
        # Open a new window to add a custom exercise
        def save_exercise():
            new_exercise = exercise_name.get()
            if new_exercise:
                self.exercise_menu['values'] = (*self.exercise_menu['values'], new_exercise)
                top.destroy()
            else:
                messagebox.showerror("Input Error", "Exercise name cannot be empty.")

        top = tk.Toplevel(self)
        top.title("Add Custom Exercise")
        top.geometry("300x100")
        top.configure(bg='#2E3440')

        exercise_label = ttk.Label(top, text="Exercise Name:")
        exercise_label.pack(pady=5)
        exercise_name = ttk.Entry(top)
        exercise_name.pack(pady=5)
        save_button = ttk.Button(top, text="Save", command=save_exercise)
        save_button.pack(pady=5)

    def log_exercise(self):
        name = self.name_var.get()
        exercise = self.exercise_var.get()
        detail = self.detail_entry.get()

        try:
            detail = float(detail)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a numeric value for reps, duration, or miles.")
            return

        calories = self.calculate_calories(exercise, detail)
        self.calories_burned += calories
        protein = self.calculate_protein(self.calories_burned)

        # Update display
        self.total_label.config(text=f"Total Calories Burned: {self.calories_burned:.2f} kcal")
        self.protein_label.config(text=f"Recommended Protein Intake: {protein:.2f} g")

        # Save to database
        self.save_to_database(name, exercise, detail, calories)

        # Clear input
        self.detail_entry.delete(0, tk.END)

    def calculate_calories(self, exercise, detail):
        # Average calories burned per unit (approximate values)
        calorie_dict = {
            # Calisthenics (calories per rep)
            "Push-ups": 0.29,
            "Pull-ups": 1.0,
            "Squats": 0.32,
            "Lunges": 0.35,
            "Planks": 5.0,  # per minute
            "Burpees": 1.5,
            "Mountain Climbers": 0.5,
            "Jumping Jacks": 0.2,
            "Sit-ups": 0.15,
            "Crunches": 0.1,

            # Cardio (calories per mile or minute)
            "Running": 100.0,  # per mile
            "Walking": 80.0,   # per mile
            "Biking": 50.0,    # per mile
            "Jump Rope": 10.0,  # per minute
            "Stair Climbing": 8.0,  # per minute
            "Elliptical": 7.0,  # per minute
            "Rowing": 7.0,      # per minute
            "Swimming": 9.0,    # per minute
            "Aerobics": 6.0,    # per minute
            "HIIT": 12.0,       # per minute

            # Weight Lifting (calories per minute)
            "Bench Press": 5.0,
            "Deadlift": 6.0,
            "Squat (Weighted)": 6.0,
            "Overhead Press": 5.0,
            "Bicep Curls": 4.0,
            "Tricep Extensions": 4.0,
            "Leg Press": 5.0,
            "Lat Pulldowns": 5.0,
            "Shoulder Press": 5.0,
            "Dumbbell Rows": 5.0,

            # Other
            "Yoga": 3.0,       # per minute
            "Pilates": 4.0,    # per minute
            "Stretching": 2.5, # per minute
            "Other": 5.0       # default value per unit
        }

        # Determine the calculation method based on exercise category
        per_unit = calorie_dict.get(exercise, 5.0)
        if exercise in ["Running", "Walking", "Biking"]:
            # Units are in miles
            calories = per_unit * detail
        elif exercise in ["Push-ups", "Pull-ups", "Squats", "Lunges", "Burpees", "Mountain Climbers", "Jumping Jacks", "Sit-ups", "Crunches"]:
            # Units are in reps
            calories = per_unit * detail
        else:
            # Units are in minutes
            calories = per_unit * detail
        return calories

    def calculate_protein(self, calories_burned):
        # General recommendation: 15g protein per 100 kcal burned
        protein_needed = (calories_burned / 100) * 15  # in grams
        return protein_needed

    def create_database(self):
        self.conn = sqlite3.connect('workout_log.db')
        self.cursor = self.conn.cursor()
        # Check if the 'name' column exists
        self.cursor.execute("PRAGMA table_info(workouts)")
        columns = [column[1] for column in self.cursor.fetchall()]
        if 'name' not in columns:
            # If the table exists but 'name' column is missing, alter the table
            try:
                self.cursor.execute("ALTER TABLE workouts ADD COLUMN name TEXT")
            except sqlite3.OperationalError:
                # If the table doesn't exist, create it
                self.cursor.execute('''
                    CREATE TABLE workouts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        exercise TEXT NOT NULL,
                        detail REAL NOT NULL,
                        calories REAL NOT NULL
                    )
                ''')
        else:
            # Create table if it doesn't exist
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS workouts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    exercise TEXT NOT NULL,
                    detail REAL NOT NULL,
                    calories REAL NOT NULL
                )
            ''')
        self.conn.commit()

    def save_to_database(self, name, exercise, detail, calories):
        self.cursor.execute('''
            INSERT INTO workouts (name, exercise, detail, calories)
            VALUES (?, ?, ?, ?)
        ''', (name, exercise, detail, calories))
        self.conn.commit()

    def on_closing(self):
        self.conn.close()
        self.destroy()

if __name__ == "__main__":
    app = WorkoutLogger()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
