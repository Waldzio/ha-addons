#!/usr/bin/env bash

# Jeśli jesteśmy pod Supervisor, pobierz poświadczenia MQTT
if command -v bashio &> /dev/null; then
  export MQTT_HOST=$(bashio::services mqtt "host")
  export MQTT_PORT=$(bashio::services mqtt "port")
  export MQTT_USER=$(bashio::services mqtt "username")
  export MQTT_PASS=$(bashio::services mqtt "password")
fi

# Uruchom główny skrypt
python3 /ping_logger.py
