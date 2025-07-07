#!/usr/bin/env bash

# Jeśli Supervisor (bashio) jest dostępny, pobierz poświadczenia:
if command -v bashio &> /dev/null; then
  export SUPERVISOR_MQTT_USERNAME=$(bashio::services mqtt "username")
  export SUPERVISOR_MQTT_PASSWORD=$(bashio::services mqtt "password")
  export SUPERVISOR_MQTT_HOST=$(bashio::services mqtt "host")
  export SUPERVISOR_MQTT_PORT=$(bashio::services mqtt "port")
fi

# Uruchom PingLogger
python3 /ping_logger.py
