import os
import time
import json
import paho.mqtt.client as mqtt
from pythonping import ping
from datetime import datetime, timedelta

CONFIG_PATH = "/data/options.json"
LOG_PATH = "/data/ping_log.json"

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def load_log():
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:
            return json.load(f)
    return {}

def save_log(log):
    with open(LOG_PATH, "w") as f:
        json.dump(log, f)

def cleanup_log(log, days):
    cutoff = datetime.now() - timedelta(days=days)
    for target in log:
        log[target] = [entry for entry in log[target] if datetime.strptime(entry["time"], "%Y-%m-%d %H:%M:%S") > cutoff]
    return log

def sanitize_topic(ip):
    return ip.replace('.', '_')

def main():
    config = load_config()
    targets = config.get("targets", [])
    interval = int(config.get("interval", 60))
    keep_days = int(config.get("keep_days", 2))
    size = int(config.get("size", 56))

    username = os.getenv("SUPERVISOR_MQTT_USERNAME")
    password = os.getenv("SUPERVISOR_MQTT_PASSWORD")
    host = os.getenv("SUPERVISOR_MQTT_HOST", "localhost")
    port = int(os.getenv("SUPERVISOR_MQTT_PORT", 1883))

    client = mqtt.Client()
    if username and password:
        client.username_pw_set(username, password)
    client.connect(host, port, 60)
    client.loop_start()

    log = load_log()
    last_values = {}

    while True:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for target in targets:
            try:
                response = ping(target, count=1, size=size, timeout=1)
                latency = round(response.rtt_avg_ms)
                print(f"Pinguje {target} ... ({latency} ms)")
            except Exception as e:
                print(f"Błąd pingu do {target}: {e}")
                latency = None

            if target not in log:
                log[target] = []

            log[target].append({"time": now, "latency": latency})
            log = cleanup_log(log, keep_days)

            if target in last_values and last_values[target] == latency:
                print(f"[STATE] Ping {target} bez zmian ({latency}), nie publikuję.")
                continue

            last_values[target] = latency

            topic = f"homeassistant/sensor/ping_{sanitize_topic(target)}/state"
            client.publish(topic, str(latency))

            discovery_topic = f"homeassistant/sensor/ping_{sanitize_topic(target)}/config"
            payload = {
                "name": f"Ping {target}",
                "state_topic": topic,
                "unit_of_measurement": "ms",
                "unique_id": f"ping_{sanitize_topic(target)}",
                "device_class": "measurement",
                "device": {
                    "identifiers": ["ping_logger"],
                    "name": "PingLogger",
                    "manufacturer": "Waldi"
                }
            }
            client.publish(discovery_topic, json.dumps(payload), retain=True)

        save_log(log)
        time.sleep(interval)

if __name__ == "__main__":
    main()
