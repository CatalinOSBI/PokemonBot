import tkinter as tk

class RegionSelector:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.wait_visibility(self.root)
        self.root.attributes('-alpha', 0.3)
        
        self.canvas = tk.Canvas(self.root, cursor="cross", bg='grey')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.text = None
        
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.root.bind("<Escape>", lambda e: self.root.quit())
        
        # Instructions
        instructions = tk.Label(
            self.root, 
            text="DRAG to select region | ESC to exit | Coords will be copied to clipboard",
            font=("Arial", 16, "bold"),
            bg="black",
            fg="white",
            pady=10
        )
        instructions.pack(side=tk.TOP, fill=tk.X)
        
    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
        if self.text:
            self.canvas.delete(self.text)
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline='red', width=3
        )
        
    def on_drag(self, event):
        cur_x, cur_y = event.x, event.y
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)
        
        # Show dimensions
        width = abs(cur_x - self.start_x)
        height = abs(cur_y - self.start_y)
        if self.text:
            self.canvas.delete(self.text)
        self.text = self.canvas.create_text(
            cur_x, cur_y + 20,
            text=f"{width} x {height}",
            fill="yellow",
            font=("Arial", 14, "bold")
        )
        
    def on_release(self, event):
        end_x, end_y = event.x, event.y
        
        # Calculate region
        left = min(self.start_x, end_x)
        top = min(self.start_y, end_y)
        width = abs(end_x - self.start_x)
        height = abs(end_y - self.start_y)
        
        # Format for Python
        region_tuple = f"region=({left}, {top}, {width}, {height})"
        
        # Copy to clipboard
        self.root.clipboard_clear()
        self.root.clipboard_append(region_tuple)
        self.root.update()
        
        # Show result
        result_text = f"Copied to clipboard:\n{region_tuple}\n\nPress ESC to exit or drag again"
        if self.text:
            self.canvas.delete(self.text)
        self.text = self.canvas.create_text(
            left + width//2, top + height//2,
            text=result_text,
            fill="lime",
            font=("Arial", 16, "bold"),
            width=400
        )
        
        print(f"\nRegion selected:")
        print(f"  Left: {left}")
        print(f"  Top: {top}")
        print(f"  Width: {width}")
        print(f"  Height: {height}")
        print(f"\nPaste this in your code:")
        print(f"  {region_tuple}")
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    print("Starting Region Selector Tool...")
    print("1. Drag to select a region on your screen")
    print("2. Coordinates will be copied to clipboard")
    print("3. Press ESC to exit\n")
    
    selector = RegionSelector()
    selector.run()