import psutil
import time

class NetWorkMonitor:
    def __init__(self):
        self.last = psutil.net_io_counters()

    def get_speed(self, interval = 1):
        time.sleep(interval)
        current = psutil.net_io_counters()

        upload = (net2.bytes_sent - net1.bytes_sent) / 1024
        download = (net2.bytes_recv - net1.bytes_recv) / 1024

        self.last = current
        return int(upload), int(download)