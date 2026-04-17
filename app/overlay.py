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

    # transparency
    root.attributes("-alpha", 0.85)

    # background
    bg_color = "#111111"

    root.configure(bg=bg_color)

    # container frame
    frame = tk.Frame(root, bg=bg_color)
    frame.pack(padx=8, pady=4)

    # download
    down_label = tk.Label(
        frame,
        text="0.0M ↓",
        font=("Segoe UI", 9),
        fg="#FFFFFF",
        bg=bg_color
    )
    down_label.pack(anchor="e")

    # upload
    up_label = tk.Label(
        frame, 
        text="0K ↑",
        font=("Segoe UI", 9),
        fg="#BBBBBB",
        bg=bg_color
    )
    up_label.pack(anchor="e")

    # position
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # position near the bottom-right
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = screen_width - 100
    y = screen_height - 50

    root.geometry(f"+{x}+{y}")

    def update():
        up, down = monitor.get_speed(interval=1)

        down_label.config(text=f"↓: {format_speed(down)}")
        up_label.config(text=f"↑: {format_speed(up)}")

        root.after(1000, update)
    
    update()
    root.mainloop()
