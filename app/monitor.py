import psutil
import time

def format_speed(speed):
    # moved from overlay to prevent duplication
    if speed >= 1024:
        return f"{speed / 1024:.1f}M"
    return f"{speed:.1f}K"

class NetworkMonitor:
    def __init__(self):
        net = psutil.net_io_counters()
        self.bytes_sent = net.bytes_sent
        self.bytes_recv = net.bytes_recv
        self.last_time = time.time()

    def get_speed(self, interval = 1):
        current = psutil.net_io_counters()
        current_time = time.time()

        # calculate actual time elapsed to prevent drift inaccuracy
        time_lapsed = current_time - self.last_time
        if time_lapsed == 0:
            # prevent division by zero
            time_lapsed = 1 


        # calculate current speed
        upload = (current.bytes_sent - self.bytes_sent) / 1024 / interval
        download = (current.bytes_recv - self.bytes_recv) / 1024 / interval

        # update stored values
        self.bytes_sent = current.bytes_sent
        self.bytes_recv = current.bytes_recv
        self.last_time = current_time

        return round(upload, 2), round(download, 2)