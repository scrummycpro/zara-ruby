import tkinter as tk
import time
import sqlite3
import random

# Randomized sentences
sentences = [
    "The cat chased the mouse around the house.",
    "In the garden, the flowers bloomed beautifully.",
    "John cooked a delicious meal for his family.",
    "Sarah played her favorite song on the guitar.",
    "The sun set behind the mountains, painting the sky in shades of pink and orange.",
    "Alex couldn't decide what to wear to the party.",
    "A group of friends went on a hiking trip in the wilderness.",
    "The old oak tree provided shade on hot summer days.",
    "Emily studied hard for her exams and aced them.",
    "The smell of freshly baked bread filled the kitchen.",
    "After the rain, a rainbow appeared in the sky.",
    "Peter spent the afternoon reading a captivating novel.",
    "Maria adopted a puppy from the animal shelter.",
    "Jack and Jill went up the hill to fetch a pail of water.",
    "The sound of waves crashing against the shore was soothing.",
    "Lisa and Tom went on a romantic dinner date.",
    "The city skyline looked mesmerizing at night.",
    "David practiced his basketball skills every day after school.",
    "Lucy enjoyed spending time outdoors, exploring nature.",
    "The smell of coffee brewing in the morning was irresistible."
]

def calculate_wpm(text, start_time, end_time):
    words = text.split()
    word_count = len(words)
    elapsed_time = (end_time - start_time) / 60  # Convert seconds to minutes
    wpm = int(word_count / elapsed_time)
    return wpm

def calculate_accuracy(typed_text, displayed_text):
    typed_words = typed_text.split()
    displayed_words = displayed_text.split()
    correct_count = sum(1 for tw, dw in zip(typed_words, displayed_words) if tw == dw)
    total_words = len(displayed_words)
    accuracy = (correct_count / total_words) * 100
    return accuracy

def start_test():
    global start_time, sentences, current_sentence_index, total_wpm, total_sentences, name
    start_time = time.time()
    current_sentence_index = 0
    total_wpm = 0
    total_sentences = 0
    name = name_entry.get()
    display_next_sentence()

def end_test():
    global start_time, total_wpm, total_sentences
    end_time = time.time()
    wpm = calculate_wpm(typing_entry.get("1.0", "end"), start_time, end_time)
    accuracy = calculate_accuracy(typing_entry.get("1.0", "end"), display_entry.get("1.0", "end-1c"))
    total_wpm += wpm
    total_sentences += 1
    wpm_label.config(text=f"Your typing speed for this sentence: {wpm} WPM")
    accuracy_label.config(text=f"Your accuracy for this sentence: {accuracy:.2f}%")
    typing_entry.delete("1.0", "end")
    if total_sentences == 5:
        average_wpm = total_wpm / 5
        wpm_label.config(text=f"Average typing speed: {average_wpm:.2f} WPM")
        accuracy_label.config(text="")
    if current_sentence_index == len(sentences):
        next_button.config(state="disabled")
    else:
        next_button.config(state="normal")

def display_next_sentence():
    global current_sentence_index
    display_entry.config(state="normal")
    display_entry.delete("1.0", "end")
    display_entry.insert("1.0", sentences[current_sentence_index])
    display_entry.config(state="disabled")
    current_sentence_index += 1
    next_button.config(state="disabled")

def highlight_text():
    typed_text = typing_entry.get("1.0", "end-1c").split()
    displayed_text = display_entry.get("1.0", "end-1c").split()
    typing_entry.tag_config("wrong", foreground="red")
    typing_entry.tag_config("correct", foreground="blue")
    for i in range(len(displayed_text)):
        if i < len(typed_text):
            if typed_text[i] == displayed_text[i]:
                typing_entry.tag_add("correct", f"1.{len(displayed_text[i-1])} wordstart", f"1.{len(displayed_text[i])} wordend")
            else:
                typing_entry.tag_add("wrong", f"1.{len(displayed_text[i-1])} wordstart", f"1.{len(displayed_text[i])} wordend")

root = tk.Tk()
root.title("Typing Speed Test")
root.configure(bg="black")

# Name Label
name_label = tk.Label(root, text="Enter your name:", fg="#FFC0CB", bg="black")  # Bubblegum Pink
name_label.pack()

# Name Entry
name_entry = tk.Entry(root)
name_entry.pack()

# Typing Entry
typing_entry = tk.Text(root, height=5, width=70, bg="black", fg="white")
typing_entry.pack(pady=10)

# Display Entry
display_entry = tk.Text(root, height=5, width=70, state="disabled", bg="black", fg="white")
display_entry.pack(pady=10)

# Start Button
start_button = tk.Button(root, text="Start Test", command=start_test, bg="#FFDAB9", fg="black")  # Peach
start_button.pack()

# End Button
end_button = tk.Button(root, text="End Test", command=end_test, bg="#FFDAB9", fg="black")  # Peach
end_button.pack()

# Next Sentence Button
next_button = tk.Button(root, text="Next Sentence", command=display_next_sentence, state="disabled", bg="#FFDAB9", fg="black")  # Peach
next_button.pack()

# WPM Label
wpm_label = tk.Label(root, text="", fg="#87CEEB", bg="black")  # Sky Blue
wpm_label.pack()

# Accuracy Label
accuracy_label = tk.Label(root, text="", fg="#87CEEB", bg="black")  # Sky Blue
accuracy_label.pack()

# Bind typing entry with text highlight function
typing_entry.bind("<KeyRelease>", lambda event: highlight_text())

root.mainloop()

