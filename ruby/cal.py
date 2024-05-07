import pyfiglet

# Create a Figlet object with a readable font
custom_fig = pyfiglet.Figlet(font='banner')

# Define rainbow color codes
rainbow_colors = [31, 33, 32, 36, 34, 35]

# Render text with rainbow colors
text = 'Calendar'
ascii_banner = ""
for i, char in enumerate(text):
    color_code = rainbow_colors[i % len(rainbow_colors)]
    ascii_banner += f"\033[38;5;{color_code}m{char}"

# Reset color
ascii_banner += "\033[0m"

# Print the ASCII art
print(custom_fig.renderText(ascii_banner))
