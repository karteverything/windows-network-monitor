from app.tray import run_tray
from app.overlay import run_overlay
import threading

if __name__ == "__main__":
    threading.Thread(
        target=run_tray,
        daemon=True
    ).start()
    
    run_overlay()