import psutil
import time
import json
from datetime import date
from pathlib import Path

# store usage data in the user's dir
USAGE_FILE = Path.home() / ".netspeedmonitor_usage.json"

def format_speed(speed):
    # moved from overlay to prevent duplication
    if speed >= 1024:
        return f"{speed / 1024:.1f}MB/s"
    return f"{speed:.1f}KB/s"

def format_data(bytes_value):
    # converts bytes into readable data units
    if bytes_value >= 1024 ** 3:
        return f"{bytes_value / (1024 ** 3):.2f} GB"

    if bytes_value >= 1024 ** 2:
        return f"{bytes_value / (1024 ** 2):.2f} MB"

    return f"{bytes_value / 1024:.2f} KB"

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

    def get_daily_usage(self):
        current = psutil.net_io_counters()
        today = str(date.today())

        # load saved data
        if USAGE_FILE.exists():
            try:
                with open(USAGE_FILE, "r") as f:
                    data = json.load(f)
            except (data.JSONDecodeError, OSError):
                data = {}
        else:
            data = {}

        # new day: create a new baseline
        if data.get("date") != today:
            data = {
                "date": today,
                "baseline_download": current.bytes_recv,
                "baseline_upload": current.bytes_sent
            }
            with open(USAGE_FILE, "w") as f:
                json.dump(data, f)

            return 0, 0

        # calculate usage since baseline
        download = (current.bytes_recv - data["baseline_download"])
        upload = (current.bytes_sent) - data["baseline_upload"]

        # handle possible network counter reset
        if download < 0: download = 0
        if upload < 0: upload = 0

        return download, upload