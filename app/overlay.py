import tkinter as tk
from app.monitor import (NetworkMonitor, format_speed, format_data)
monitor = NetworkMonitor()

def run_overlay():

    root = tk.Tk()
    # Remove window borders
    root.overrideredirect(True)
    # Always on top
    root.attributes("-topmost", True)
    # Transparency
    root.attributes("-alpha", 0.85)
    bg_color = "#111111"
    root.configure(bg=bg_color)

    WINDOW_WIDTH = 105
    WINDOW_HEIGHT = 45

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = screen_width - WINDOW_WIDTH - 20
    y = screen_height - WINDOW_HEIGHT - 60

    root.geometry(
        f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}"
    )
    root.pack_propagate(False)

    # -----------------------------
    # DRAGGING
    # -----------------------------
    def start_move(event):
        root.x = event.x
        root.y = event.y

    def stop_move(event):
        root.x = None
        root.y = None

    def do_move(event):
        deltax = event.x - root.x
        deltay = event.y - root.y

        new_x = root.winfo_x() + deltax
        new_y = root.winfo_y() + deltay

        root.geometry(
            f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{new_x}+{new_y}"
        )

    root.bind("<ButtonPress-1>", start_move)
    root.bind("<ButtonRelease-1>", stop_move)
    root.bind("<B1-Motion>", do_move)

    # -----------------------------
    # RIGHT-CLICK MENU
    # -----------------------------
    context_menu = tk.Menu(
        root,
        tearoff=0,
        bg="black",
        fg="white"
    )

    context_menu.add_command(
        label="Exit Monitor",
        command=root.destroy
    )

    def show_menu(event):
        context_menu.tk_popup(
            event.x_root,
            event.y_root
        )
    root.bind("<Button-3>", show_menu)

    # -----------------------------
    # MAIN FRAME
    # -----------------------------
    frame = tk.Frame(
        root,
        bg=bg_color
    )

    frame.pack(
        expand=True,
        fill="both",
        padx=6,
        pady=2
    )

    frame.columnconfigure(1, weight=1)

    # DOWNLOAD LABEL
    down_label = tk.Label(
        frame,
        text="↓:",
        font=("Consolas", 9),
        fg="#FFFFFF",
        bg=bg_color
    )
    down_label.grid(
        row=1,
        column=0,
        sticky="w"
    )

    # DOWNLOAD SPEED
    down_speed = tk.Label(
        frame,
        text="0 KB/s",
        font=("Consolas", 9),
        fg="#FFFFFF",
        bg=bg_color,
        anchor="e"
    )
    down_speed.grid(
        row=1,
        column=1,
        sticky="e"
    )

    # UPLOAD LABEL
    up_label = tk.Label(
        frame,
        text="↑:",
        font=("Consolas", 9),
        fg="#BBBBBB",
        bg=bg_color
    )
    up_label.grid(
        row=0,
        column=0,
        sticky="w"
    )
    # UPLOAD SPEED
    up_speed = tk.Label(
        frame,
        text="0 KB/s",
        font=("Consolas", 9),
        fg="#BBBBBB",
        bg=bg_color,
        anchor="e"
    )
    up_speed.grid(
        row=0,
        column=1,
        sticky="e"
    )

    # -----------------------------
    # HOVER TOOLTIP
    # -----------------------------
    tooltip = None

    def show_tooltip(event=None):
        nonlocal tooltip

        if tooltip is not None:
            return

        tooltip = tk.Toplevel(root)
        tooltip.overrideredirect(True)
        tooltip.attributes("-topmost", True)
        tooltip.attributes("-alpha", 0.95)
        tooltip.configure(bg="#222222")

        # Tooltip content frame
        tooltip_frame = tk.Frame(
            tooltip,
            bg="#222222",
            padx=10,
            pady=8
        )

        tooltip_frame.pack()

        # Title
        title = tk.Label(
            tooltip_frame,
            text="Today's Usage",
            font=("Consolas", 10, "bold"),
            fg="#FFFFFF",
            bg="#222222"
        )
        title.pack(anchor="w")

        # Download usage
        download_label = tk.Label(
            tooltip_frame,
            text="Download: 0.00 GB",
            font=("Consolas", 9),
            fg="#FFFFFF",
            bg="#222222"
        )
        download_label.pack(anchor="w")

        # Upload usage
        upload_label = tk.Label(
            tooltip_frame,
            text="Upload:   0.00 GB",
            font=("Consolas", 9),
            fg="#BBBBBB",
            bg="#222222"
        )
        upload_label.pack(anchor="w")

        # Total usage
        total_label = tk.Label(
            tooltip_frame,
            text="Total:    0.00 GB",
            font=("Consolas", 9),
            fg="#00FF99",
            bg="#222222"
        )
        total_label.pack(anchor="w")

        # Position tooltip above overlay
        tooltip.update_idletasks()
        tooltip_width = tooltip.winfo_width()
        tooltip_height = tooltip.winfo_height()

        overlay_x = root.winfo_x()
        overlay_y = root.winfo_y()

        tooltip_x = overlay_x + WINDOW_WIDTH - tooltip_width
        tooltip_y = overlay_y - tooltip_height - 5

        tooltip.geometry(
            f"+{tooltip_x}+{tooltip_y}"
        )

        def update_tooltip():
            if tooltip is None or not tooltip.winfo_exists():
                return

            download, upload = monitor.get_daily_usage()
            total = download + upload

            download_label.config(
                text=f"Download: {format_data(download)}"
            )
            upload_label.config(
                text=f"Upload:   {format_data(upload)}"
            )
            total_label.config(
                text=f"Total:    {format_data(total)}"
            )
            tooltip.after(1000, update_tooltip)
        update_tooltip()

    def hide_tooltip(event=None):
        nonlocal tooltip

        if tooltip is not None:
            tooltip.destroy()
            tooltip = None

    # Bind hover events to main window and widgets
    widgets = [
        root,
        frame,
        down_label,
        down_speed,
        up_label,
        up_speed
    ]

    for widget in widgets:
        widget.bind(
            "<Enter>",
            show_tooltip
        )
        widget.bind(
            "<Leave>",
            hide_tooltip
        )

    # -----------------------------
    # SPEED UPDATE
    # -----------------------------
    def update():
        up, down = monitor.get_speed()

        down_speed.config(
            text=format_speed(down)
        )
        up_speed.config(
            text=format_speed(up)
        )

        root.after(
            1000,
            update
        )
    update()
    root.mainloop()