import pyfiglet

# Create a Figlet object
custom_fig = pyfiglet.Figlet(font='slant')

# Render text
ascii_banner = custom_fig.renderText('Zaras Mind!')

# Print the ASCII art
print(ascii_banner)
