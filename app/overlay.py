import tkinter as tk
from app.monitor import NetworkMonitor, format_speed

monitor = NetworkMonitor()

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

    # define explicit dimensions
    WINDOW_WIDTH = 90
    WINDOW_HEIGHT = 45

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = screen_width - WINDOW_WIDTH - 20
    y = screen_height - WINDOW_HEIGHT - 60

    # set fixed width and height in grometry
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")

    # prevent child widgets from changing root window size
    root.pack_propagate(False)

    # dragging func (fixed size while dragging)
    def start_move(event):
        root.x = event.x
        root.y = event.y

    def stop_move(event):
        root.x = None
        root.y = None

    def do_move(event):
        deltax = event.x - root.x 
        deltay = event.y - root.y 
        x = root.winfo_x() + deltax
        y = root.winfo_y() + deltay
        root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")

    # bind dragging and right-click to exit
    root.bind("<ButtonPress-1>", start_move)
    root.bind("<ButtonRelease-1>", stop_move)
    root.bind("<B1-Motion>", do_move)
    
    # create right-click menu
    context_menu = tk.Menu(root, tearoff=0, bg="black", fg="white")
    context_menu.add_command(label="Exit Monitor", command=root.destroy)

    def show_menu(event):
        context_menu.tk_popup(event.x_root, event.y_root)

    # bind righ-click to show menu instead of instant exit
    root.bind("<Button-3>", show_menu)

    # container frame
    frame = tk.Frame(root, bg=bg_color)
    frame.pack(expand=True, fill="both", padx=6, pady=4)

    # download
    down_label = tk.Label(
        frame,
        text="0.0 ↓",
        font=("Consolas", 9),
        fg="#FFFFFF",
        bg=bg_color
    )
    down_label.pack(anchor="e")

    # upload
    up_label = tk.Label(
        frame, 
        text="0 ↑",
        font=("Consolas", 9),
        fg="#BBBBBB",
        bg=bg_color
    )
    up_label.pack(anchor="e")

    root.update_idletasks()

    # position near the bottom-right
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = screen_width - 100
    y = screen_height - 60

    root.geometry(f"+{x}+{y}")

    def update():
        up, down = monitor.get_speed()
        down_label.config(text=f"↓: {format_speed(down)}")
        up_label.config(text=f"↑: {format_speed(up)}")
        root.after(1000, update)
    
    update()
    root.mainloop()
