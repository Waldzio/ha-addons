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
        return json.load(open(LOGFILE))
    return {}

def save_log(log):
    json.dump(log, open(LOGFILE, "w"))

def cleanup(log, days):
    cutoff = datetime.now() - timedelta(days=days)
    for ip in list(log):
        log[ip] = [e for e in log[ip] if datetime.fromisoformat(e["time"]) > cutoff]
    return log

def sanitize(ip): return ip.replace(".", "_")

def main():
    cfg = load_config()
    targets = cfg["targets"]
    interval, keep, size = map(int, (cfg["interval"], cfg["keep_days"], cfg["size"]))

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
            log = cleanup(log, keep)

            if last.get(ip) != rtt:
                last[ip] = rtt
                topic = f"homeassistant/sensor/ping_{sanitize(ip)}"
                client.publish(f"{topic}/state", rtt or "timeout", retain=True)
                cfgt = {
                    "name": f"Ping {ip}",
                    "state_topic": f"{topic}/state",
                    "unit_of_measurement": "ms",
                    "unique_id": f"ping_{sanitize(ip)}",
                    "device_class": "measurement",
                    "device": {"identifiers":["ping_logger"],"name":"PingLogger","manufacturer":"Waldi"}
                }
                client.publish(f"{topic}/config", json.dumps(cfgt), retain=True)
        save_log(log)
        time.sleep(interval)

if __name__ == "__main__":
    main()
