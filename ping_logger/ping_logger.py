import os
import time
import json
import paho.mqtt.client as mqtt
from pythonping import ping
from datetime import datetime, timedelta

# Ścieżka do opcji i logów
CONFIG_PATH = "/data/options.json"
LOG_FILE = "/data/ping_log.json"

def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)

# ... (funkcje logowania i czyszczenia jak wcześniej) ...

def main():
    cfg = load_config()
    targets = cfg.get("targets", [])
    interval = int(cfg.get("interval", 60))
    keep_days = int(cfg.get("keep_days", 2))
    size = int(cfg.get("size", 56))

    # Poświadczenia z Bashio (Supervisor)
    host = os.getenv("MQTT_HOST", "localhost")
    port = int(os.getenv("MQTT_PORT", 1883))
    user = os.getenv("MQTT_USER", "")
    pwd = os.getenv("MQTT_PASS", "")

    client = mqtt.Client()
    if user:
        client.username_pw_set(user, pwd)
    client.connect(host, port)
    client.loop_start()

    # ... (reszta pętli pingowania) ...
