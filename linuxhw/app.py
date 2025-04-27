import tkinter as tk
import random
import pyttsx3
import sqlite3

# ----------------------------
# SETUP TTS ENGINE (clear woman’s voice)
# ----------------------------
engine = pyttsx3.init()
engine.setProperty('rate', 120)
engine.setProperty('volume', 1.0)

voices = engine.getProperty('voices')
for voice in voices:
    if 'female' in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

def speak(text):
    engine.say(text)
    engine.runAndWait()

def speak_full_word(word):
    # First, speak the full word
    speak(word)
    # Then, spell the word with hyphens in between each letter
    spelled_out = '-'.join(list(word))
    speak(spelled_out)

# ----------------------------
# SETUP DATABASE
# ----------------------------
conn = sqlite3.connect("reading_scores.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT,
    typed TEXT,
    correct INTEGER
)
""")
conn.commit()

def save_result(word, typed, correct):
    cursor.execute("INSERT INTO grades (word, typed, correct) VALUES (?, ?, ?)", (word, typed, correct))
    conn.commit()

def save_final_grade(correct_count, total_words):
    grade = (correct_count / total_words) * 100
    cursor.execute("INSERT INTO grades (word, typed, correct) VALUES (?, ?, ?)", ("Final Grade", str(grade), correct_count))
    conn.commit()

# ----------------------------
# WORDS SETUP
# ----------------------------
word_list = ['cat', 'dog', 'sun', 'hat', 'apple', 'ball', 'fish', 'tree', 'book', 'car']
words = random.sample(word_list, 5)
current_index = 0
correct_count = 0  # To keep track of correct answers

# ----------------------------
# GUI SETUP
# ----------------------------
root = tk.Tk()
root.title("Reading Practice")
root.geometry("600x400")
root.configure(bg="#121212")

# UI ELEMENTS
instruction = tk.Label(root, text="Click 'Speak Word' to begin the practice.", font=("Helvetica Neue", 16), bg="#121212", fg="#ffffff")
instruction.pack(pady=10)

speak_btn = tk.Button(root, text="🔊 Speak Word", font=("Helvetica Neue", 16), bg="#1e1e1e", fg="#90e0ef", command=lambda: on_speak())
speak_btn.pack(pady=5)

feedback = tk.Label(root, text="", font=("Helvetica Neue", 18), bg="#121212", fg="#ffffff")
feedback.pack(pady=5)

entry = tk.Entry(root, font=("Helvetica Neue", 22), justify="center", bg="#333333", fg="#ffffff", insertbackground="white")
entry.pack(pady=10)

# ----------------------------
# LABEL FOR SPELLING UNDER INPUT BOX
# ----------------------------
spelled_out = tk.Label(root, text="", font=("Courier New", 20), bg="#121212", fg="#6a4c93")
spelled_out.pack(pady=10)

# ----------------------------
# BUTTON FOR SUBMISSION
# ----------------------------
def on_speak():
    word = words[current_index]
    spelled = ' '.join(list(word))  # Display spelling below input box
    spelled_out.config(text=f"Spelling: {spelled.upper()}")  # Show spelling under input box
    speak_full_word(word)  # Speak the full word and then spell it out

def check_word():
    global current_index, correct_count
    typed = entry.get().strip().lower()
    correct_word = words[current_index]

    if typed == correct_word:
        feedback.config(text="✅ Correct!", fg="green")
        speak("Correct! Great job!")
        save_result(correct_word, typed, 1)
        correct_count += 1  # Increase correct answers count
        current_index += 1
        entry.delete(0, tk.END)

        if current_index < len(words):
            spelled_out.config(text="")
        else:
            feedback.config(text="🎉 You finished!", fg="blue")
            spelled_out.config(text="")
            speak("You finished all the words. Well done!")
            save_final_grade(correct_count, len(words))  # Save the final grade

    else:
        feedback.config(text="❌ Try again!", fg="red")
        speak("That's not correct. Try again.")
        save_result(correct_word, typed, 0)

submit_btn = tk.Button(root, text="Submit", font=("Helvetica Neue", 16), bg="#333333", fg="#90e0ef", command=check_word)
submit_btn.pack(pady=5)

# Start with welcome
speak("Welcome! Click Speak Word to begin.")

root.mainloop()
