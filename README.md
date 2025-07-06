# LAN to WAN Relationss – Home Assistant Add-on

This add-on monitors selected IP addresses by pinging them at configurable intervals.
Each address is represented as a separate sensor in Home Assistant via MQTT discovery.

Features:
- Pings custom IP addresses at user-defined intervals.
- Logs ping times to CSV for history and analysis.
- Sends sensor values only if ping result changes (rounded to full milliseconds).
- Full MQTT Discovery support for easy integration.
- Works with MQTT user and password (Home Assistant user).
- Configuration available in the GUI.

Installation:
1. Copy the `lan_to_wan_relationss` folder and `repository.json` to your custom add-ons repository.
2. Add the repo to Home Assistant as a custom add-on repository.
3. Configure via GUI (IP addresses, interval, log retention, MQTT credentials).
4. Done! Sensors will show up automatically.