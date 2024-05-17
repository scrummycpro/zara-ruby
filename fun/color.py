import tkinter as tk
import random
import pyperclip

def generate_color():
    # Generate random values for RGB
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)
    
    # Format the RGB values into a hexadecimal color code
    color_code = "#{:02x}{:02x}{:02x}".format(red, green, blue)
    
    # Update the label text and background color
    color_label.config(text=color_code, bg=color_code)

def show_color():
    color_code = color_entry.get()
    if is_valid_color_code(color_code):
        color_label.config(text=color_code, bg=color_code)
    else:
        color_label.config(text="Invalid color code", bg="white")

def is_valid_color_code(color_code):
    if len(color_code) != 7 or color_code[0] != '#' or not all(c in '0123456789abcdefABCDEF' for c in color_code[1:]):
        return False
    return True

def copy_color():
    color_code = color_label.cget("text")
    pyperclip.copy(color_code)

# Create the main window
root = tk.Tk()
root.title("Color Generator")

# Create a label to display the color code
color_label = tk.Label(root, text="", font=("Helvetica", 16), padx=20, pady=10)
color_label.pack()

# Create a button to generate a random color
generate_button = tk.Button(root, text="Generate Random Color", font=("Helvetica", 14), command=generate_color)
generate_button.pack(pady=10)

# Create an entry for user to input color code
color_entry = tk.Entry(root, font=("Helvetica", 14))
color_entry.pack(pady=10)

# Create a button to show color from input
show_color_button = tk.Button(root, text="Show Color", font=("Helvetica", 14), command=show_color)
show_color_button.pack(pady=10)

# Create a button to copy color code to clipboard
copy_button = tk.Button(root, text="Copy Color Code", font=("Helvetica", 14), command=copy_color)
copy_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
