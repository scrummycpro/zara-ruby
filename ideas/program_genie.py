import tkinter as tk
import random

class ProgrammingIdeaGenerator:
    def __init__(self, master):
        self.master = master
        master.title("Programming Idea Generator")
        master.geometry("400x300")
        master.configure(background='#000000')

        self.python_ideas = [
            "Create a calculator",
            "Implement a To-Do list manager",
            "Build a simple weather app",
            "Develop a basic chat application",
            "Write a program to generate random passwords",
            "Implement a basic file encryption tool",
            "Design a basic note-taking app",
            "Create a simple text editor",
            "Develop a basic file manager",
            "Write a program to search for files by name",
            "Implement a basic image viewer",
            "Design a simple calendar app",
            "Create a basic contact manager",
            "Develop a program to convert units",
            "Write a program to calculate BMI",
            "Implement a basic expense tracker",
            "Design a simple stopwatch",
            "Create a program to generate QR codes",
            "Develop a basic currency converter",
            "Write a program to generate random quotes",
            "Implement a basic URL shortener",
            "Design a program to calculate age in days",
            "Create a basic countdown timer",
            "Develop a program to check internet speed",
            "Write a program to generate ASCII art",
            "Implement a basic text-based RPG game",
            "Design a simple password generator",
            "Create a program to sort files by extension",
            "Develop a basic web scraper",
            "Write a program to generate random numbers",
            "Implement a basic RSS feed reader",
            "Design a program to calculate average grades",
            "Create a basic barcode generator",
            "Develop a program to generate strong passwords",
            "Write a program to analyze text sentiment",
            "Implement a basic file organizer",
            "Design a program to find duplicate files",
            "Create a simple task scheduler",
            "Develop a program to parse JSON data",
            "Write a program to check if a number is prime",
            "Implement a basic image editor",
            "Design a program to extract text from images",
            "Create a basic recipe manager",
            "Develop a program to track daily water intake",
            "Write a program to generate random usernames",
            "Implement a basic music player",
            "Design a program to calculate tip",
            "Create a simple drawing application",
            "Develop a program to calculate compound interest",
            "Write a program to calculate factorial",
            "Implement a basic password manager",
            "Design a program to track daily steps",
            "Create a basic quiz application",
            "Develop a program to check spelling",
            "Write a program to generate lorem ipsum text",
            "Implement a basic chess game",
            "Design a program to generate random colors",
            "Create a simple file backup tool",
            "Develop a program to analyze website SEO",
            "Write a program to generate fractals",
            "Implement a basic encryption/decryption tool",
            "Design a program to calculate tip splitting",
            "Create a simple budget planner",
            "Develop a program to generate CAPTCHA images",
            "Write a program to generate random mazes",
            "Implement a basic password strength checker",
            "Design a program to create custom calendars",
            "Create a basic image watermarking tool",
            "Develop a program to generate QR codes with logo",
            "Write a program to solve quadratic equations",
            "Implement a basic file compression tool",
            "Design a program to calculate tip splitting",
            "Create a simple budget planner",
            "Develop a program to generate CAPTCHA images",
            "Write a program to generate random mazes",
            "Implement a basic password strength checker",
            "Design a program to create custom calendars",
            "Create a basic image watermarking tool",
            "Develop a program to generate QR codes with logo",
            "Write a program to solve quadratic equations",
            "Implement a basic file compression tool",
            "Design a program to calculate tip splitting",
            "Create a simple budget planner",
            "Develop a program to generate CAPTCHA images",
            "Write a program to generate random mazes",
            "Implement a basic password strength checker",
            "Design a program to create custom calendars",
            "Create a basic image watermarking tool",
            "Develop a program to generate QR codes with logo",
            "Write a program to solve quadratic equations",
            "Implement a basic file compression tool"
        ]

        self.ruby_ideas = [
            "Create a blogging platform",
            "Build a URL shortener service",
            "Implement a basic inventory management system",
            "Develop a simple forum application",
            "Design a task management tool",
            "Create a simple note-taking app",
            "Build a basic file manager",
            "Implement a program to search for files by name",
            "Develop a basic image viewer",
            "Design a simple calendar app",
            "Create a basic contact manager",
            "Build a program to convert units",
            "Implement a basic expense tracker",
            "Develop a simple stopwatch",
            "Design a program to generate QR codes",
            "Create a basic currency converter",
            "Build a program to generate random quotes",
            "Implement a basic URL shortener",
            "Develop a program to calculate age in days",
            "Design a simple password generator",
            "Create a program to sort files by extension",
            "Build a basic web scraper",
            "Implement a program to generate random numbers",
            "Develop a basic RSS feed reader",
            "Design a program to calculate average grades",
            "Create a simple task scheduler",
            "Build a program to parse JSON data",
            "Implement a basic file organizer",
            "Develop a program to find duplicate files",
            "Design a simple recipe manager",
            "Create a basic barcode generator",
            "Build a program to generate strong passwords",
            "Implement a basic image editor",
            "Develop a program to extract text from images",
            "Design a simple drawing application",
            "Create a basic music player",
            "Build a program to calculate tip",
            "Implement a basic password manager",
            "Develop a program to track daily steps",
            "Design a simple quiz application",
            "Create a program to check spelling",
            "Build a program to generate lorem ipsum text",
            "Implement a basic chess game",
            "Develop a program to generate random colors",
            "Design a simple file backup tool",
            "Create a basic pomodoro timer",
            "Build a program to analyze website traffic",
            "Implement a basic encryption/decryption tool",
            "Develop a program to track daily expenses",
            "Design a simple image slideshow",
            "Create a basic file compression tool",
            "Build a program to calculate distance between cities",
            "Implement a basic chatbot",
            "Develop a program to create custom calendars",
            "Design a simple password strength checker",
            "Create a program to generate word clouds",
            "Build a basic expense report generator",
            "Implement a program to analyze Twitter sentiment",
            "Develop a program to solve quadratic equations",
            "Design a simple crossword puzzle generator",
            "Create a basic budget planner",
            "Build a program to track daily calories",
            "Implement a basic file encryption tool",
            "Develop a program to calculate greatest common divisor",
            "Design a simple horoscope generator",
            "Create a program to generate random mazes",
            "Build a basic password-protected diary",
            "Implement a program to analyze stock market trends",
            "Develop a program to generate random geometric shapes"
        ]

        self.idea_label = tk.Label(master, text="", bg='#000000', fg='white', font=('Helvetica', 12))
        self.idea_label.pack(pady=20)

        self.python_button = tk.Button(master, text="Python Idea", command=self.generate_python_idea, bg='teal', font=('Helvetica', 10))
        self.python_button.pack(side=tk.LEFT, padx=20)

        self.ruby_button = tk.Button(master, text="Ruby Idea", command=self.generate_ruby_idea, bg='teal', font=('Helvetica', 10))
        self.ruby_button.pack(side=tk.RIGHT, padx=20)

        self.close_button = tk.Button(master, text="Close", command=master.quit, bg='teal', font=('Helvetica', 10))
        self.close_button.pack(side=tk.BOTTOM, pady=20)

    def generate_python_idea(self):
        idea = random.choice(self.python_ideas)
        self.idea_label.config(text=idea)

    def generate_ruby_idea(self):
        idea = random.choice(self.ruby_ideas)
        self.idea_label.config(text=idea)

def main():
    root = tk.Tk()
    app = ProgrammingIdeaGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
