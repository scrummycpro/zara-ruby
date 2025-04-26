import tkinter as tk
from tkinter import messagebox
import sqlite3

class PottyTrainingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Potty Training App")
        self.root.geometry("400x400")
        self.root.configure(bg="black")

        # Dark theme colors
        self.bg_color = "#2e2e2e"
        self.fg_color = "#ffffff"
        self.button_color = "#444444"
        self.button_text_color = "#ffffff"
        
        self.stars = 0  # Track how many stars the child earns
        self.create_database()

        # Title label
        self.title_label = tk.Label(root, text="Potty Training!", font=("Arial", 24, "bold"), bg=self.bg_color, fg=self.fg_color)
        self.title_label.pack(pady=20)

        # Instructions
        self.instruction_label = tk.Label(root, text="Press the button after using the potty!", font=("Arial", 14), bg=self.bg_color, fg=self.fg_color)
        self.instruction_label.pack(pady=10)

        # Potty button
        self.potty_button = tk.Button(root, text="Used the Potty!", font=("Arial", 16), bg=self.button_color, fg=self.button_text_color, command=self.on_potty_used)
        self.potty_button.pack(pady=20)

        # Star count label
        self.star_label = tk.Label(root, text=f"Stars: {self.stars}", font=("Arial", 16), bg=self.bg_color, fg=self.fg_color)
        self.star_label.pack(pady=10)

        # Reset button
        self.reset_button = tk.Button(root, text="Reset Stars", font=("Arial", 14), bg=self.button_color, fg=self.button_text_color, command=self.reset_stars)
        self.reset_button.pack(pady=10)

    def create_database(self):
        """Create the SQLite database if it doesn't exist."""
        self.conn = sqlite3.connect("potty_training.db")
        self.cursor = self.conn.cursor()

        # Create the table to store star count and prize info
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS progress (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               stars INTEGER,
                               prize TEXT)''')
        self.conn.commit()

    def save_progress(self):
        """Save the current star count and prize to the database."""
        prize = self.get_prize(self.stars)
        self.cursor.execute("INSERT INTO progress (stars, prize) VALUES (?, ?)", (self.stars, prize))
        self.conn.commit()

    def get_prize(self, stars):
        """Return a prize based on the number of stars."""
        if stars >= 5 and stars < 10:
            return "Snack"
        elif stars >= 10 and stars < 15:
            return "Toy"
        elif stars >= 15:
            return "Special Gift"
        else:
            return "No Prize Yet"

    def on_potty_used(self):
        """Increase star count when the child uses the potty."""
        self.stars += 1
        self.star_label.config(text=f"Stars: {self.stars}")
        
        # Show a congratulatory message
        messagebox.showinfo("Good Job!", "You did it! Here's a star!")
        
        # Check if a prize is earned
        prize = self.get_prize(self.stars)
        if prize != "No Prize Yet":
            messagebox.showinfo("Prize Earned!", f"Congrats! You earned a {prize}!")
            self.save_progress()  # Save progress when prize is earned
            self.stars = 0  # Reset stars after receiving prize
            self.star_label.config(text=f"Stars: {self.stars}")

    def reset_stars(self):
        """Reset the star count."""
        self.stars = 0
        self.star_label.config(text=f"Stars: {self.stars}")
        messagebox.showinfo("Reset", "Stars have been reset.")

    def __del__(self):
        """Close the database connection when the app is closed."""
        self.conn.close()

# Set up the root Tkinter window
root = tk.Tk()

# Create the PottyTrainingApp
app = PottyTrainingApp(root)

# Run the Tkinter event loop
root.mainloop()
