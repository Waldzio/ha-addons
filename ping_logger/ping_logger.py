import os, time, json
from datetime import datetime, timedelta
from pythonping import ping
import paho.mqtt.client as mqtt

CONFIG = "/data/options.json"
LOGFILE = "/data/ping_log.json"

def load_config():
    with open(CONFIG) as f: return json.load(f)

def load_log():
    if os.path.exists(LOGFILE):
        with open(LOGFILE) as f: return json.load(f)
    return {}

def save_log(log):
    with open(LOGFILE, "w") as f: json.dump(log, f)

def cleanup(log, days):
    cutoff = datetime.now() - timedelta(days=days)
    for ip, arr in log.items():
        log[ip] = [e for e in arr if datetime.fromisoformat(e["time"]) > cutoff]
    return log

def sanitize(ip): return ip.replace(".", "_")

def main():
    cfg = load_config()
    targets   = cfg.get("targets", [])
    interval  = int(cfg.get("interval", 60))
    keep_days = int(cfg.get("keep_days", 2))
    size      = int(cfg.get("size", 56))

    host = os.getenv("MQTT_HOST", cfg.get("mqtt_host", "localhost"))
    port = int(os.getenv("MQTT_PORT", cfg.get("mqtt_port", 1883)))
    user = os.getenv("MQTT_USER", cfg.get("mqtt_user", ""))
    pwd  = os.getenv("MQTT_PASS", cfg.get("mqtt_pass", ""))

    client = mqtt.Client()
    if user: client.username_pw_set(user, pwd)
    client.connect(host, port)
    client.loop_start()

    log = load_log()
    last = {}

    while True:
        now = datetime.now().isoformat()
        for ip in targets:
            try:
                res = ping(ip, count=1, size=size, timeout=1)
                rtt = int(round(res.rtt_avg_ms)) if res.success() else None
            except:
                rtt = None

            log.setdefault(ip, []).append({"time": now, "latency": rtt})
            log = cleanup(log, keep_days)

            if last.get(ip) == rtt:
                continue
            last[ip] = rtt

            topic_state = f"homeassistant/sensor/ping_{sanitize(ip)}/state"
            client.publish(topic_state, rtt if rtt is not None else "timeout", retain=True)

            topic_cfg = f"homeassistant/sensor/ping_{sanitize(ip)}/config"
            payload = {
                "name": f"Ping {ip}",
                "state_topic": topic_state,
                "unit_of_measurement": "ms",
                "unique_id": f"ping_{sanitize(ip)}",
                "device_class": "measurement",
                "device": {
                    "identifiers": ["ping_logger"],
                    "name": "PingLogger",
                    "manufacturer": "Waldi"
                }
            }
            client.publish(topic_cfg, json.dumps(payload), retain=True)

        save_log(log)
        time.sleep(interval)

if __name__ == "__main__":
    main()
