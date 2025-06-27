import tkinter as tk
import sqlite3
import random

# Connect to SQLite database (create table with correct columns)
conn = sqlite3.connect("science_test_results.db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS results
    (name TEXT, score INTEGER, letter_grade TEXT)
''')
conn.commit()

# Your 60 questions as tuples (question, options list, correct answer)
question_bank = [
    ("What planet is known as the Red Planet?", ["Venus", "Earth", "Mars", "Jupiter"], "Mars"),
    ("Which gas do plants use for photosynthesis?", ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"], "Carbon Dioxide"),
    ("What is the chemical symbol for water?", ["O2", "CO2", "H2O", "NaCl"], "H2O"),
    ("How many planets are in our solar system?", ["7", "8", "9", "10"], "8"),
    ("What force keeps us on the ground?", ["Magnetism", "Inertia", "Gravity", "Friction"], "Gravity"),
    ("Which organ pumps blood?", ["Lungs", "Kidney", "Brain", "Heart"], "Heart"),
    ("Which planet is the largest?", ["Earth", "Saturn", "Jupiter", "Neptune"], "Jupiter"),
    ("What part of the cell holds DNA?", ["Nucleus", "Mitochondria", "Ribosome", "Cytoplasm"], "Nucleus"),
    ("Boiling point of water (°C)?", ["90", "95", "100", "105"], "100"),
    ("Which vitamin comes from sunlight?", ["A", "B", "C", "D"], "D"),
    ("What tool measures temperature?", ["Barometer", "Thermometer", "Scale", "Timer"], "Thermometer"),
    ("What is the center of an atom?", ["Proton", "Neutron", "Nucleus", "Electron"], "Nucleus"),
    ("Which planet has rings?", ["Venus", "Mars", "Saturn", "Mercury"], "Saturn"),
    ("What's the largest bone in the body?", ["Femur", "Humerus", "Skull", "Spine"], "Femur"),
    ("What gas do we breathe in?", ["Carbon Dioxide", "Oxygen", "Helium", "Nitrogen"], "Oxygen"),
    ("What causes day and night?", ["Revolution", "Tides", "Rotation", "Sunlight"], "Rotation"),
    ("What organ filters blood?", ["Lungs", "Liver", "Heart", "Kidney"], "Kidney"),
    ("Which is a renewable resource?", ["Oil", "Coal", "Sunlight", "Natural Gas"], "Sunlight"),
    ("Main source of Earth’s energy?", ["Moon", "Wind", "Sun", "Volcanoes"], "Sun"),
    ("Which is NOT a state of matter?", ["Solid", "Liquid", "Gas", "Energy"], "Energy"),
    ("Which blood cells fight infection?", ["Red", "White", "Platelets", "Plasma"], "White"),
    ("Which body system controls actions?", ["Skeletal", "Digestive", "Respiratory", "Nervous"], "Nervous"),
    ("Which is a chemical change?", ["Melting", "Freezing", "Burning", "Boiling"], "Burning"),
    ("What animal is a mammal?", ["Frog", "Snake", "Whale", "Shark"], "Whale"),
    ("Which is a vertebrate?", ["Insect", "Octopus", "Cat", "Worm"], "Cat"),
    ("What is a lunar eclipse?", ["Moon blocks sun", "Earth blocks sun", "Earth blocks moon", "Sun blocks moon"], "Earth blocks moon"),
    ("Which has gills?", ["Dog", "Fish", "Bird", "Lizard"], "Fish"),
    ("How long is Earth's rotation?", ["24 hrs", "365 days", "7 days", "12 hrs"], "24 hrs"),
    ("What does DNA stand for?", ["Digital Nucleic Acid", "Data Neural Agent", "Deoxyribonucleic Acid", "Dynamic Nucleic Acid"], "Deoxyribonucleic Acid"),
    ("What organ digests food?", ["Heart", "Lungs", "Stomach", "Kidney"], "Stomach"),
    ("Which simple machine is a ramp?", ["Lever", "Pulley", "Inclined Plane", "Wedge"], "Inclined Plane"),
    ("Where does photosynthesis happen?", ["Roots", "Stem", "Leaves", "Flower"], "Leaves"),
    ("What carries messages in the body?", ["Blood", "Nerves", "Bones", "Muscles"], "Nerves"),
    ("What kind of energy is in food?", ["Chemical", "Thermal", "Nuclear", "Mechanical"], "Chemical"),
    ("What does a prism do?", ["Bend sound", "Split light", "Heat water", "Store energy"], "Split light"),
    ("What does an insulator do?", ["Blocks heat", "Creates energy", "Conducts electricity", "Stores light"], "Blocks heat"),
    ("What type of rock is granite?", ["Igneous", "Sedimentary", "Metamorphic", "Fossil"], "Igneous"),
    ("How many legs does an insect have?", ["6", "8", "4", "10"], "6"),
    ("Which planet is closest to the Sun?", ["Venus", "Earth", "Mercury", "Mars"], "Mercury"),
    ("What’s used to measure mass?", ["Thermometer", "Scale", "Timer", "Meter stick"], "Scale"),
    ("Which is a conductor?", ["Rubber", "Wood", "Metal", "Plastic"], "Metal"),
    ("What causes seasons?", ["Earth's distance", "Sun's movement", "Earth's tilt", "Moon's phases"], "Earth's tilt"),
    ("What’s the pH of water?", ["3", "5", "7", "10"], "7"),
    ("What is static electricity?", ["Flow of current", "Charge build-up", "Heat wave", "Light energy"], "Charge build-up"),
    ("How do bats navigate?", ["Sight", "Smell", "Touch", "Echolocation"], "Echolocation"),
    ("What do we call baby frogs?", ["Tadpoles", "Chicks", "Cubs", "Larvae"], "Tadpoles"),
    ("Which planet is icy and blue?", ["Mars", "Uranus", "Venus", "Mercury"], "Uranus"),
    ("Where is magma found?", ["Sky", "Ocean", "Underground", "Desert"], "Underground"),
    ("What is wind?", ["Moving air", "Heat waves", "Water flow", "Sound wave"], "Moving air"),
    ("Which object reflects light?", ["Mirror", "Black shirt", "Water", "Rock"], "Mirror"),
    ("What layer protects Earth?", ["Crust", "Mantle", "Ozone", "Core"], "Ozone"),
    ("What is metamorphosis?", ["Sleeping", "Hibernation", "Growth change", "Migration"], "Growth change"),
    ("Which organ helps you breathe?", ["Heart", "Liver", "Lung", "Stomach"], "Lung"),
    ("Which is a non-renewable resource?", ["Sun", "Coal", "Wind", "Water"], "Coal"),
    ("Which moon phase is fully lit?", ["New Moon", "Half Moon", "Full Moon", "Crescent"], "Full Moon"),
    ("Which is a producer?", ["Lion", "Mushroom", "Tree", "Frog"], "Tree"),
    ("What helps muscles move?", ["Calcium", "Iron", "Protein", "Fat"], "Protein"),
    ("What planet has a big red spot?", ["Earth", "Jupiter", "Mars", "Venus"], "Jupiter"),
    ("What animal is cold-blooded?", ["Human", "Dog", "Snake", "Bird"], "Snake"),
    ("What is condensation?", ["Gas to solid", "Liquid to gas", "Gas to liquid", "Solid to liquid"], "Gas to liquid")
]

class ScienceTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("8th Grade Science Test")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        
        # Matte dark gray background
        self.bg_color = "#2f2f2f"
        self.root.configure(bg=self.bg_color)

        # Frame for padding and content
        self.frame = tk.Frame(root, bg=self.bg_color, padx=20, pady=20)
        self.frame.pack(expand=True, fill="both")

        # User name input
        self.name_label = tk.Label(self.frame, text="Enter Your Name:", font=("Arial", 16), fg="#90caf9", bg=self.bg_color)
        self.name_label.pack(pady=(0,10))
        self.name_entry = tk.Entry(self.frame, font=("Arial", 14))
        self.name_entry.pack(pady=(0,20))

        # Start button
        self.start_button = tk.Button(self.frame, text="Start Test", font=("Arial", 14), command=self.start_test, bg="#455a64", fg="white", activebackground="#90caf9", padx=10, pady=5)
        self.start_button.pack()

        # Question and options
        self.question_label = None
        self.option_buttons = []
        self.submit_button = None
        self.feedback_label = None
        
        self.current_question = 0
        self.score = 0
        self.questions = []

        # End screen buttons (restart/exit)
        self.restart_button = None
        self.exit_button = None

    def start_test(self):
        name = self.name_entry.get().strip()
        if not name:
            self.name_label.config(text="Please enter your name!", fg="red")
            return
        self.username = name
        self.name_label.pack_forget()
        self.name_entry.pack_forget()
        self.start_button.pack_forget()

        self.score = 0
        self.current_question = 0
        self.questions = random.sample(question_bank, 10)  # 10 questions randomly

        self.show_question()

    def show_question(self):
        if self.current_question >= len(self.questions):
            self.finish_test()
            return

        # Clear previous widgets
        if self.question_label:
            self.question_label.destroy()
        for btn in self.option_buttons:
            btn.destroy()
        if self.submit_button:
            self.submit_button.destroy()
        if self.feedback_label:
            self.feedback_label.destroy()
        
        q = self.questions[self.current_question]
        question_text = q[0]
        options = q[1]

        self.question_label = tk.Label(self.frame, text=f"Q{self.current_question + 1}: {question_text}", font=("Arial", 16), fg="white", bg=self.bg_color, wraplength=650, justify="left")
        self.question_label.pack(pady=(0,15))

        self.selected_option = tk.StringVar(value="")

        self.option_buttons = []
        for option in options:
            rb = tk.Radiobutton(self.frame, text=option, variable=self.selected_option, value=option,
                                font=("Arial", 14), bg=self.bg_color, fg="white", selectcolor="#90caf9",
                                activebackground="#455a64", activeforeground="white", pady=5)
            rb.pack(anchor="w", padx=20)
            self.option_buttons.append(rb)

        self.submit_button = tk.Button(self.frame, text="Submit Answer", command=self.submit_answer, bg="#455a64", fg="white", font=("Arial", 14), padx=10, pady=5)
        self.submit_button.pack(pady=20)

        self.feedback_label = tk.Label(self.frame, text="", font=("Arial", 14), fg="#90caf9", bg=self.bg_color)
        self.feedback_label.pack()

    def submit_answer(self):
        selected = self.selected_option.get()
        if not selected:
            self.feedback_label.config(text="Please select an answer!", fg="red")
            return

        correct = self.questions[self.current_question][2]
        if selected == correct:
            self.score += 10
            self.feedback_label.config(text="Correct! 🎉", fg="#4caf50")
        else:
            self.feedback_label.config(text=f"Wrong! ❌ The correct answer was: {correct}", fg="#f44336")

        self.submit_button.config(state="disabled")
        for btn in self.option_buttons:
            btn.config(state="disabled")

        # After 2 seconds, go to next question
        self.root.after(2000, self.next_question)

    def next_question(self):
        self.current_question += 1
        self.show_question()

    def finish_test(self):
        # Clear question widgets
        if self.question_label:
            self.question_label.destroy()
        for btn in self.option_buttons:
            btn.destroy()
        if self.submit_button:
            self.submit_button.destroy()
        if self.feedback_label:
            self.feedback_label.destroy()

        # Calculate grade
        grade = self.calculate_grade(self.score)

        # Save to database
        cursor.execute("INSERT INTO results (name, score, letter_grade) VALUES (?, ?, ?)",
                       (self.username, self.score, grade))
        conn.commit()

        # Show final score and grade
        self.final_label = tk.Label(self.frame, text=f"Test Completed!\n\n{self.username}, you scored {self.score}/100.\nYour grade: {grade}",
                                    font=("Arial", 18), fg="white", bg=self.bg_color, pady=20)
        self.final_label.pack()

        # Restart and Exit buttons
        self.restart_button = tk.Button(self.frame, text="Take Another Test", font=("Arial", 14), bg="#455a64", fg="white", padx=10, pady=5, command=self.restart_test)
        self.restart_button.pack(pady=(30,10))

        self.exit_button = tk.Button(self.frame, text="Exit", font=("Arial", 14), bg="#455a64", fg="white", padx=10, pady=5, command=self.root.quit)
        self.exit_button.pack()

    def calculate_grade(self, score):
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"

    def restart_test(self):
        # Clear final widgets
        self.final_label.destroy()
        self.restart_button.destroy()
        self.exit_button.destroy()

        # Show name entry again
        self.name_label.config(text="Enter Your Name:", fg="#90caf9")
        self.name_label.pack(pady=(0,10))
        self.name_entry.delete(0, tk.END)
        self.name_entry.pack(pady=(0,20))
        self.start_button.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = ScienceTestApp(root)
    root.mainloop()
