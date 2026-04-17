import psutil
import time

class NetWorkMonitor:
    def __init__(self):
        self.last = psutil.net_io_counters()

    def get_speed(self, interval = 1):
        time.sleep(interval)
        current = psutil.net_io_counters()

        upload = (current.bytes_sent - self.bytes_sent) / 1024
        download = (current.bytes_recv - self.bytes_recv) / 1024

        self.last = current
        return int(upload), int(download)