from PIL import Image, ImageDraw, ImageFont
import random

def generate_image():
    # Create a new image with white background
    width, height = 800, 600
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    # Generate golden hearts
    for _ in range(50):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(10, 30)
        draw.ellipse([(x, y), (x+size, y+size)], fill=(255, 215, 0))

    # Generate ocean
    draw.rectangle([(0, height//2), (width, height)], fill=(0, 191, 255))

    # Generate flowers
    for _ in range(30):
        x = random.randint(0, width)
        y = random.randint(height//2, height)
        size = random.randint(5, 15)
        draw.ellipse([(x, y), (x+size, y+size)], fill=(255, 192, 203))

    # Generate mountains
    for _ in range(100):
        x = random.randint(0, width)
        y = random.randint(0, height//2)
        size = random.randint(10, 30)
        draw.polygon([(x, y), (x+size, y+size*2), (x+size*2, y)], fill=(128, 128, 128))

    # Add your name in cursive at the top right corner
    font = ImageFont.truetype("arial.ttf", 20)
    name = "Your Name"
    text_width, text_height = draw.textsize(name, font=font)
    draw.text((width - text_width - 10, 10), name, fill="#fb7a45", font=font)

    # Show the image
    image.show()

    # Ask user if they want to save the image
    save = input("Do you want to save this image? (yes/no): ").lower()
    if save == "yes":
        image.save("generated_image.png")
        print("Image saved as 'generated_image.png'")
    else:
        print("Image not saved.")

if __name__ == "__main__":
    generate_image()
