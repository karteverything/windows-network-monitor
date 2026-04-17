import psutil
import time

def get_speed(interval = 1):
    net1 = psutil.net_io_counters()
    time.sleep(interval)
    net2 = psutil.net_io_counters()

    upload = (net2.bytes_sent - net1.bytes_sent) / 1024
    download = (net2.bytes_recv - net1.bytes_recv) / 1024

    return int(upload), int(download)