import tkinter as tk
from datetime import datetime, timedelta

class CountdownTimer:
    def __init__(self, minutes):
        self.root = tk.Tk()
        self.root.title("Countdown Timer")

        self.time_left = timedelta(minutes=minutes)
        self.label = tk.Label(self.root, font=('Helvetica', 48))
        self.label.pack(padx=20, pady=20)

        self.update_display()
        self.start_timer()

    def update_display(self):
        self.label.config(text=str(self.time_left))
        if self.time_left.total_seconds() == 0:
            self.label.config(text="Time's up!")
        else:
            self.root.after(1000, self.update_timer)

    def update_timer(self):
        self.time_left -= timedelta(seconds=1)
        self.update_display()

    def start_timer(self):
        self.root.mainloop()

# Set the countdown time in minutes
countdown_time = 5
timer = CountdownTimer(countdown_time)
