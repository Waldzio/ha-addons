import os
import json
import asyncio
import csv
from datetime import datetime, timedelta
from pythonping import ping as py_ping

CONFIG_PATH = "/data/options.json"
LOG_FILE = "/data/ping_logger.csv"

# Wczytaj config z Supervisor Addon
with open(CONFIG_PATH) as f:
    conf = json.load(f)

TARGETS = conf.get("targets", ["8.8.8.8"])
INTERVAL = int(conf.get("interval", 1))
KEEP_DAYS = int(conf.get("keep_days", 2))

def log_ping(ip, rtt):
    with open(LOG_FILE, "a") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().isoformat(), ip, rtt if rtt is not None else "timeout"])

def cleanup_logs(days):
    if not os.path.exists(LOG_FILE):
        return
    cutoff = datetime.now() - timedelta(days=days)
    with open(LOG_FILE, "r") as f:
        rows = list(csv.reader(f))
    new_rows = [row for row in rows if row and datetime.fromisoformat(row[0]) > cutoff]
    with open(LOG_FILE, "w") as f:
        writer = csv.writer(f)
        writer.writerows(new_rows)

async def main_loop():
    while True:
        for ip in TARGETS:
            try:
                resp = py_ping(ip, count=1, timeout=1)
                if resp.success():
                    rtt = resp.rtt_avg_ms
                else:
                    rtt = None
            except Exception as e:
                rtt = None
            log_ping(ip, rtt)
        cleanup_logs(KEEP_DAYS)
        await asyncio.sleep(INTERVAL)

if __name__ == "__main__":
    asyncio.run(main_loop())
