import tkinter as tk
from tkinter import ttk, colorchooser

class ZPaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ZPaint")

        self.pen_color = "black"
        self.brush_size = 5
        self.brush_shape = "circle"
        self.blender_active = False

        self.canvas = tk.Canvas(self.root, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.setup_tools()

        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<Shift-Button-1>", self.activate_blender)
        self.canvas.bind("<KeyRelease-Shift>", self.deactivate_blender)

    def setup_tools(self):
        self.color_btn = ttk.Button(self.root, text="Color", command=self.choose_color)
        self.color_btn.pack(side=tk.LEFT)

        self.clear_btn = ttk.Button(self.root, text="Clear", command=self.clear_canvas)
        self.clear_btn.pack(side=tk.LEFT)

        self.size_frame = ttk.Frame(self.root)
        self.size_frame.pack(side=tk.LEFT, padx=5)
        
        self.size_label = ttk.Label(self.size_frame, text="Brush Size:")
        self.size_label.pack(side=tk.LEFT)
        
        self.size_scale = ttk.Scale(self.size_frame, from_=1, to=20, orient=tk.HORIZONTAL, command=self.change_brush_size)
        self.size_scale.set(self.brush_size)
        self.size_scale.pack(side=tk.LEFT)
        
        self.blender_btn = ttk.Checkbutton(self.root, text="Blender", command=self.toggle_blender)
        self.blender_btn.pack(side=tk.LEFT)

    def choose_color(self):
        color = colorchooser.askcolor(title="Choose color")
        if color:
            self.pen_color = color[1]

    def change_brush_size(self, val):
        self.brush_size = int(val)

    def paint(self, event):
        if self.blender_active:
            self.blend_color(event)
        else:
            self.draw(event)

    def draw(self, event):
        x1, y1 = (event.x - self.brush_size), (event.y - self.brush_size)
        x2, y2 = (event.x + self.brush_size), (event.y + self.brush_size)
        if self.brush_shape == "circle":
            self.canvas.create_oval(x1, y1, x2, y2, fill=self.pen_color, outline=self.pen_color)
        elif self.brush_shape == "square":
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.pen_color, outline=self.pen_color)

    def activate_blender(self, event):
        self.blender_active = True

    def deactivate_blender(self, event):
        self.blender_active = False

    def blend_color(self, event):
        items = self.canvas.find_overlapping(event.x - self.brush_size, event.y - self.brush_size,
                                              event.x + self.brush_size, event.y + self.brush_size)
        for item in items:
            if self.canvas.type(item) == "rectangle" or self.canvas.type(item) == "oval":
                current_color = self.canvas.itemcget(item, "fill")
                blended_color = self.blend_colors(current_color, self.pen_color)
                self.canvas.itemconfig(item, fill=blended_color)

    def blend_colors(self, color1, color2):
        r1, g1, b1 = self.hex_to_rgb(color1)
        r2, g2, b2 = self.hex_to_rgb(color2)
        r = (r1 + r2) // 2
        g = (g1 + g2) // 2
        b = (b1 + b2) // 2
        return f'#{r:02x}{g:02x}{b:02x}'

    def hex_to_rgb(self, hex_color):
        return tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))

    def clear_canvas(self):
        self.canvas.delete("all")
        
    def toggle_blender(self):
        self.blender_active = not self.blender_active

def main():
    root = tk.Tk()
    app = ZPaintApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
