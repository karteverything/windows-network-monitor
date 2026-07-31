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
    threading.Thread(
        target=update_icon, 
        args=(icon,), 
        daemon=True
    ).start()
    
    
def run_tray():
    # check if icon exists
    if not ICON_PATH.exists():
        raise FileNotFoundError(
            f"Could not find icon: \n{ICON_PATH}"
        )

    icon_image = Image.open(ICON_PATH)
    
    # attach 'quit app' to menu
    menu = pystray.Menu(
        item('Quit', quit_action)
    )
    
    # create initial icon
    # pass icon at creation time
    tray_icon = pystray.Icon(
        "NetworkMonitor", 
        icon_image,
        "Network Monitor",
        menu,
    )

    tray_icon.run(setup=setup)
    


