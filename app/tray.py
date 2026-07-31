import threading
from PIL import Image, ImageDraw
import pystray
from pystray import MenuItem as item
from app.monitor import NetworkMonitor, format_speed
import time
import os

monitor = NetworkMonitor()

def create_icon(text):
    # create small icon 
    img = Image.new("RGB", (64, 64), (20, 20, 20))
    draw = ImageDraw.Draw(img)
    # basic font
    draw.text((5, 10), text, fill="white")

    return img

def update_icon(icon):
    # stops thread if icon is closed
    while True: 
        try:
            up, down = monitor.get_speed()

            # format speed
            text = (
                f"↑: {format_speed(up)}\n"
                f"↓: {format_speed(down)}"
            )
            icon.icon = create_icon(text)

            time.sleep(1)

        except Exception as e:
            print("Error updating icon:", e)
            time.sleep(1)

def quit_action(icon):
    icon.stop()
    os._exit(0)

# strart updating in background thread
def setup(icon):
    threading.Thread(
        target=update_icon, 
        args=(icon,), 
        daemon=True
    ).start()
    
    
def run_tray():
    # add menu so user can quit the app
    menu = pystray.Menu(
        item('Quit', quit_action)
    )
    
    # create initial icon
    # pass icon at creation time
    icon = pystray.Icon(
        "NetSpeed", 
        create_icon("0↓\n0↑"),
        "Network Monitor",
        menu
    )

    icon.run(setup=setup)
    


