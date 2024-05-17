from PIL import Image, ImageDraw

# Create a new image with white background
image = Image.new("RGB", (400, 300), "white")

# Create a draw object
draw = ImageDraw.Draw(image)

# Draw a rectangle
draw.rectangle((50, 50, 200, 200), fill="blue", outline="black")

# Save the image
image.save("rectangle_image.png")

# Show the image (optional)
image.show()
