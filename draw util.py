import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import calc

class ImageRectDrawer:
    def __init__(self, root):
        self.root = root
        self.root.title("Rectangle Drawer")
        
        # Load an image
        self.canvas = tk.Canvas(root)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Variables to store rectangle info
        self.rectangles = []
        self.start_x = None
        self.start_y = None
        self.current_rect = None

        # Buttons for undo and export
        self.undo_button = tk.Button(root, text="Undo", command=self.undo_last)
        self.undo_button.pack(side=tk.LEFT)
        self.export_button = tk.Button(root, text="Export", command=self.export_rectangles)
        self.export_button.pack(side=tk.LEFT)
        
        # Load and display image
        self.image_path = filedialog.askopenfilename(filetypes=[("JPG files", "*.jpg")])
        self.load_image(self.image_path)
        
        # Bind events
        self.canvas.bind("<ButtonPress-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def load_image(self, path):
        self.image = Image.open(path)
        
        # Scale image down to fit the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        img_width, img_height = self.image.size
        scale_factor = min(screen_width / img_width, screen_height / img_height, 1)
        new_size = (int(img_width * scale_factor), int(img_height * scale_factor))
        
        self.scaled_image = self.image.resize(new_size)
        self.tk_image = ImageTk.PhotoImage(self.scaled_image)
        self.canvas.config(width=new_size[0], height=new_size[1])
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def on_click(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.current_rect = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline="red")

    def on_drag(self, event):
        if self.current_rect:
            self.canvas.coords(self.current_rect, self.start_x, self.start_y, event.x, event.y)

    def on_release(self, event):
        if self.current_rect:
            x1, y1, x2, y2 = self.canvas.coords(self.current_rect)
            self.rectangles.append((x1, y1, x2, y2))
            self.current_rect = None

    def undo_last(self):
        if self.rectangles:
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
            self.rectangles.pop()
            for rect in self.rectangles:
                self.canvas.create_rectangle(rect[0], rect[1], rect[2], rect[3], outline="red")

    def export_rectangles(self):
        if not self.rectangles:
            messagebox.showinfo("Info", "No rectangles to export!")
            return
        
        # Export rectangle coordinates
        rect_str_list = [f"{int(x1)},{int(y1)},{int(x2)},{int(y2)}" for x1, y1, x2, y2 in self.rectangles]


        export_str = "\n".join(rect_str_list)
        calc_list = export_str.split("\n")
        tuple_data = [tuple(map(int, item.split(','))) for item in calc_list]
        
        print(calc.generate_html(tuple_data))

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageRectDrawer(root)
    root.mainloop()
