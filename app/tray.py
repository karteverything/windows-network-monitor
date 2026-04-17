import threading
from PIL import Image, ImageDraw, ImageFont
import pystray
from app.monitor import NetWorkMonitor
import time

monitor = NetWorkMonitor()

def create_icon(text):
    # create small icon 
    img = Image.new("RGB", (64, 64), (20, 20, 20))
    draw = ImageDraw.Draw(img)

    # basic font
    draw.text((5, 10), text, fill="white")

    return img

def format_speed(speed):
    if speed > 1024:
        return f"{speed/1024:.1f}M"
    return f"{speed}K"

def update_icon(icon):
    while True:
        try:
            up, down = monitor.get_speed()

            # format text (KB/s)
            text = f"{format_speed(down)}↓\n{format_speed(up)}↑"

            icon.icon = create_icon(text)
            icon.title = f"Download: {down} KB/s | Upload: {up} KB/s"

            time.sleep(1)

        except Exception as e:
            print("Error updating icon:", e)
            time.sleep(1)

def run_tray():
    # create initial icon
    # pass icon at creation time
    icon = pystray.Icon("NetSpeed", create_icon("0↓\n0↑"))

    # strart updating in background thread
    thread = threading.Thread(target=update_icon, args=(icon,), daemon=True)
    thread.start()

    icon.run()
