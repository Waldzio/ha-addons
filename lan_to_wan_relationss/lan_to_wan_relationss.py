import os
import json
import time
import csv
from datetime import datetime, timedelta
from pythonping import ping
import paho.mqtt.client as mqtt

CONFIG_PATH = "/data/options.json"
LOG_FILE = "/data/lan_to_wan_relationss.csv"

print("=== [LAN TO WAN RELATIONSS START] ===")
print("Loading config from", CONFIG_PATH)
try:
    with open(CONFIG_PATH) as f:
        conf = json.load(f)
    print("Config loaded:", conf)
except Exception as e:
    print("Error loading config:", e)
    raise SystemExit(1)

TARGETS = conf.get("targets", ["8.8.8.8"])
INTERVAL = int(conf.get("interval", 2))
KEEP_DAYS = int(conf.get("keep_days", 2))
MQTT_HOST = conf.get("mqtt_host", "localhost")
MQTT_PORT = int(conf.get("mqtt_port", 1883))
MQTT_USER = conf.get("mqtt_user", "")
MQTT_PASS = conf.get("mqtt_pass", "")

DISCOVERY_PREFIX = 'homeassistant'
DEVICE_NAME = 'lan_to_wan_relationss'

def log_ping(ip, rtt):
    try:
        with open(LOG_FILE, "a") as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().isoformat(), ip, rtt if rtt is not None else "timeout"])
    except Exception as e:
        print(f"Error logging ping {ip}: {e}")

def cleanup_logs(days):
    try:
        if not os.path.exists(LOG_FILE):
            return
        cutoff = datetime.now() - timedelta(days=days)
        with open(LOG_FILE, "r") as f:
            rows = list(csv.reader(f))
        new_rows = [row for row in rows if row and datetime.fromisoformat(row[0]) > cutoff]
        with open(LOG_FILE, "w") as f:
            writer = csv.writer(f)
            writer.writerows(new_rows)
    except Exception as e:
        print(f"Error cleaning logs: {e}")

def mqtt_publish_discovery(client, ip):
    sensor_id = f"lan_to_wan_{ip.replace('.', '_')}"
    topic_cfg = f"{DISCOVERY_PREFIX}/sensor/{sensor_id}/config"
    topic_state = f"{DISCOVERY_PREFIX}/sensor/{sensor_id}/state"

    payload_cfg = {
        "name": f"LAN to WAN {ip}",
        "state_topic": topic_state,
        "unit_of_measurement": "ms",
        "unique_id": sensor_id,
        "device_class": "measurement",
        "device": {
            "identifiers": [DEVICE_NAME],
            "name": "LAN to WAN Relationss",
            "manufacturer": "Waldi"
        }
    }
    print(f"[DISCOVERY] Publishing discovery to {topic_cfg}: {payload_cfg}")
    client.publish(topic_cfg, json.dumps(payload_cfg), retain=True)

def main():
    print("Connecting to MQTT:", MQTT_HOST, MQTT_PORT)
    try:
        client = mqtt.Client(protocol=mqtt.MQTTv311)
        if MQTT_USER:
            client.username_pw_set(MQTT_USER, MQTT_PASS)
        client.connect(MQTT_HOST, MQTT_PORT)
        print("Connected to MQTT")
        client.loop_start()
    except Exception as e:
        print("MQTT connection error:", e)
        raise SystemExit(2)

    # Publish discovery at start, only once!
    for ip in TARGETS:
        mqtt_publish_discovery(client, ip)

    last_values = {}  # Remember last ping value for each IP

    print("Starting ping loop...")
    while True:
        for ip in TARGETS:
            print(f"Pinging {ip} ...")
            try:
                resp = ping(ip, count=1, timeout=1)
                if resp.success():
                    rtt = int(round(resp.rtt_avg_ms))
                else:
                    rtt = "timeout"
            except Exception as e:
                print(f"Ping error for {ip}: {e}")
                rtt = "timeout"

            log_ping(ip, rtt)

            prev = last_values.get(ip, None)
            if rtt != prev:
                topic_state = f"{DISCOVERY_PREFIX}/sensor/lan_to_wan_{ip.replace('.', '_')}/state"
                print(f"[STATE] {ip}: sending state: {rtt} (previous: {prev})")
                client.publish(topic_state, str(rtt), retain=True)
                last_values[ip] = rtt
            else:
                print(f"[STATE] {ip}: no change, not sending (last: {prev})")
        cleanup_logs(KEEP_DAYS)
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()