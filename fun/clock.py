import subprocess
import tkinter as tk
import time  # Import the time module
from PIL import Image, ImageTk

class TimerApp:
    def __init__(self, master):
        self.master = master
        master.title("Timer & Music Player")

        self.timer_running = False

        # Load background image
        background_path = "/home/richmack/ruby/fun/heart.jpeg"
        self.background_image = Image.open(background_path)
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(master, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Style for buttons
        button_style = {'background': 'gold'}

        self.timer_label = tk.Label(master, text="Timer: 00:00", bg='gold')
        self.timer_label.pack()

        self.start_button = tk.Button(master, text="Start Timer", command=self.start_timer, **button_style)
        self.start_button.pack()

        self.stop_button = tk.Button(master, text="Stop Timer", command=self.stop_timer, **button_style)
        self.stop_button.pack()
        self.stop_button.config(state=tk.DISABLED)

        self.play_button = tk.Button(master, text="Play Music", command=self.play_music, **button_style)
        self.play_button.pack()

        self.stop_music_button = tk.Button(master, text="Stop Music", command=self.stop_music, **button_style)
        self.stop_music_button.pack()
        self.stop_music_button.config(state=tk.DISABLED)

        self.load_triangle()

    def load_triangle(self):
        # Load the triangle image
        triangle_path = "/home/richmack/ruby/fun/heart.jpeg"
        self.triangle_image = Image.open(triangle_path)
        self.triangle_photo = ImageTk.PhotoImage(self.triangle_image)
        self.triangle_label = tk.Label(self.master, image=self.triangle_photo)
        self.triangle_label.pack()

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.stop_music_button.config(state=tk.DISABLED)
            self.play_button.config(state=tk.DISABLED)
            for t in range(60, -1, -1):
                minutes = t // 60
                seconds = t % 60
                time_str = "{:02d}:{:02d}".format(minutes, seconds)
                self.timer_label.config(text="Timer: " + time_str)
                self.master.update()
                time.sleep(1)
                if not self.timer_running:  # Check if stop button is pressed
                    break
            self.timer_running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.play_button.config(state=tk.NORMAL)
            self.stop_music_button.config(state=tk.NORMAL)
            if not self.timer_running:
                self.play_music()

    def stop_timer(self):
        self.timer_running = False

    def play_music(self):
        song_path = "/home/richmack/Music/RAC_-_It's_A_Shame_(Best_Part_Loop)_Xavier_Thorpe_edit___[Wednesday]-vcYlify6FRo.mp3"
        self.music_process = subprocess.Popen(["mplayer", song_path])
        self.play_button.config(state=tk.DISABLED)
        self.stop_music_button.config(state=tk.NORMAL)

    def stop_music(self):
        self.music_process.terminate()
        self.play_button.config(state=tk.NORMAL)
        self.stop_music_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
