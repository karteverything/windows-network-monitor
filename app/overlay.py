import tkinter as tk
from app.monitor import NetWorkMonitor

monitor = NetWorkMonitor()

def format_speed(speed):
    if speed > 1024:
        return f"{speed/1024:.1f}M"
    return f"{speed}K"

def run_overlay():
    root = tk.Tk()

    # remove window borders
    root.overrideredirect(True)

    # always on top
    root.attributes("-topmost", True)

    # transparent background
    # root.config(bg="black")
    root.attributes("-alpha", 0.85)

    label = tk.Label(
        root, 
        text="0K↓ 0K↑",
        font=("Segoe UI", 8),
        fg="black",
        # bg="black"
    )
    label.pack()

    # position near the bottom-right
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = screen_width - 360
    y = screen_height - 35

    root.geometry(f"+{x}+{y}")

    def update():
        up, down = monitor.get_speed(interval=1)

        text = f"↓: {format_speed(down)} ↑: {format_speed(up)}"
        label.config(text=text)

        root.after(1000, update)
    
    update()
    root.mainloop()
