import threading
from PIL import Image, ImageDraw, ImageFont
import pystray
from app.monitor import NetWorkMonitor

monitor = NetWorkMonitor()

def create_icon(text):
    # create small icon 
    img = Image.new("RGB", (64, 64), (20, 20, 20))
    draw = ImageDraw.Draw(img)

    # basic font
    draw.text((5, 10), text, fill="white")

    return img

def update_icon(icon):
    while True:
        up, down = monitor.get_speed()

        # format text (KB/s)
        text = f"{down}↓\n{up}↑"

        icon.icon = create_icon(text)
        icon.title = f"Download: {down} KB/s | Upload: {up} KB/s"

def run_tray():
    icon = pystray.Icon("NetSpeed")

    # strart updating in background thread
    thread = threading.Thread(target=update_icon, args=(icon,), daemon=True)
    thread.start()

    icon.run()
    