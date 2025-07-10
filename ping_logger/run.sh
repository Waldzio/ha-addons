#!/usr/bin/env bash

if command -v bashio &> /dev/null; then
  export MQTT_HOST=$(bashio::services mqtt "host")
  export MQTT_PORT=$(bashio::services mqtt "port")
  export MQTT_USER=$(bashio::services mqtt "username")
  export MQTT_PASS=$(bashio::services mqtt "password")
fi

/venv/bin/python /ping_logger.py
