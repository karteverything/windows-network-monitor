import psutil

class NetWorkMonitor:
    def __init__(self):
        net = psutil.net_io_counters()
        self.bytes_sent = net.bytes_sent
        self.bytes_recv = net.bytes_recv

    def get_speed(self, interval = 1):
        current = psutil.net_io_counters()

        upload = (current.bytes_sent - self.bytes_sent) / 1024
        download = (current.bytes_recv - self.bytes_recv) / 1024

        # update stored values
        self.bytes_sent = current.bytes_sent
        self.bytes_recv = current.bytes_recv

        return round(upload, 2), round(download, 2)