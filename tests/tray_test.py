from PIL import Image
import pystray

image = Image.new("RGB", (64, 64), "blue")

icon = pystray.Icon(
    "Test",
    image,
    "Tray Test"
)

icon.run()