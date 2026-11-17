import threading
from PIL import Image, ImageDraw
import pystray
from pystray import MenuItem as item
from app.monitor import NetworkMonitor, format_speed
import time
import os
from pathlib import Path

# define image path
BASE_DIR = Path(__file__).resolve().parent.parent
ICON_PATH = BASE_DIR / "assets" / "icon.png"

monitor = NetworkMonitor()

def update_icon(icon):
    # stops thread if icon is closed
    while True: 
        try:
            up, down = monitor.get_speed()

            # format speed
            icon.title = (
                f"↑: {format_speed(up)}\n"
                f"↓: {format_speed(down)}"
            )
            # update every second
            time.sleep(1)

        except Exception as e:
            print("Tray error:", e)
            time.sleep(1)

# quits app
def quit_action(icon):
    icon.stop()
    os._exit(0)

# called once tray icon is visible
def setup(icon):
    # make tray icon visible in taskbar
    icon.visible = True

    # start the background speed-update thread
    threading.Thread(
        target=update_icon, 
        args=(icon,), 
        daemon=True
    ).start()
    
    
def run_tray(command_queue):
    if not ICON_PATH.exists():
        raise FileNotFoundError(
            f"Could not find icon: \n{ICON_PATH}"
        )

    print("1. Loading tray image...")
    icon_image = Image.open(ICON_PATH)

    print("2. Creating tray menu...")

    def restore_action(icon, item):
        command_queue.put("restore")

    menu = pystray.Menu(
        item('Open', restore_action, default=True),
        item('Quit', quit_action)
    )

    print("3. Creating tray icon...")

    tray_icon = pystray.Icon(
        "NetworkMonitor",
        icon_image,
        "Network Monitor",
        menu,
    )

    print("4. Starting tray icon...")
    tray_icon.run(setup=setup)

    print("5. Tray icon stopped.")