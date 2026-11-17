import threading
import queue

from app.tray import run_tray
from app.overlay import run_overlay

if __name__ == "__main__":
    # shared communication channel
    command_queue = queue.Queue()

    # start system tray in the background thread
    threading.Thread(
        target=run_tray,
        args=(command_queue,),
        daemon=True
    ).start()

    # start overlay in the main thread
    run_overlay(command_queue)