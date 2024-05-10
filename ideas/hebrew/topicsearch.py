import tkinter as tk
from tkinter import messagebox, Menu, filedialog
import sqlite3
from datetime import datetime
import subprocess
import json

def save_to_database(timestamp, word, response):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('topic_search.db')
        cursor = conn.cursor()

        # Create a table if not exists
        cursor.execute('''CREATE TABLE IF NOT EXISTS searches (
                            id INTEGER PRIMARY KEY,
                            timestamp TEXT,
                            word TEXT,
                            response TEXT
                        )''')

        # Insert timestamp, word, and response into the table
        cursor.execute("INSERT INTO searches (timestamp, word, response) VALUES (?, ?, ?)", (timestamp, word, response))
        conn.commit()

        # Close the connection
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def search_word(word):
    # Define the command
    command = f"curl --request GET --url https://www.sefaria.org/api/name/{word} --header 'accept: application/json'"

    # Execute the command
    try:
        result = subprocess.run(command.split(), capture_output=True, text=True)
        json_result = json.loads(result.stdout)

        # Extract timestamp from the JSON result
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Save timestamp, word, and response to the database
        save_to_database(timestamp, word, json.dumps(json_result))

        # Display the result
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        decoded_result = json.dumps(json_result, indent=4, ensure_ascii=False)
        result_text.insert(tk.END, decoded_result)
        result_text.config(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while searching for the word: {e}")

def search_button_clicked():
    word = search_entry.get()
    if word:
        search_word(word)
    else:
        messagebox.showwarning("Warning", "Please enter a word to search.")

def save_as_json():
    try:
        result = result_text.get("1.0", tk.END)
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(result)
            messagebox.showinfo("Success", "Search results saved as JSON file.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving JSON file: {e}")

# Create the GUI
root = tk.Tk()
root.title("Topic Search")
root.geometry("800x600")

# Search label and entry
search_frame = tk.Frame(root)
search_frame.pack(pady=10)

search_label = tk.Label(search_frame, text="Enter topic to search:")
search_label.pack(side=tk.LEFT, padx=5)

search_entry = tk.Entry(search_frame, width=50)
search_entry.pack(side=tk.LEFT, padx=5)

search_button = tk.Button(search_frame, text="Search", command=search_button_clicked)
search_button.pack(side=tk.LEFT, padx=5)

# Save as JSON button
save_button = tk.Button(root, text="Save as JSON", command=save_as_json)
save_button.pack(pady=5)

# Result text area with scroll bar
result_frame = tk.Frame(root)
result_frame.pack(pady=5, fill=tk.BOTH, expand=True)

result_text = tk.Text(result_frame, height=20, width=80)
result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(result_frame, command=result_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
result_text.config(yscrollcommand=scrollbar.set)

# Context menu for result text area (right-click to paste)
context_menu = Menu(result_text, tearoff=0)
context_menu.add_command(label="Paste", command=lambda: result_text.event_generate("<Control-v>"))
result_text.bind("<Button-3>", lambda event: context_menu.post(event.x_root, event.y_root))

root.mainloop()

