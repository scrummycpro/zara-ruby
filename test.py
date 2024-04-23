import pyfiglet

# Create a Figlet object
custom_fig = pyfiglet.Figlet(font='slant')

# Define the cyan color code
cyan_color_code = 36

# Render text with cyan color
text = 'Zaras Mind!'
ascii_banner = f"\033[38;5;{cyan_color_code}m{custom_fig.renderText(text)}"

# Reset color
ascii_banner += "\033[0m"

# Print the ASCII art
print(ascii_banner)
