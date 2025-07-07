#!/usr/bin/with-contenv bashio
export SUPERVISOR_MQTT_USERNAME=$(bashio::services "mqtt" "username")
export SUPERVISOR_MQTT_PASSWORD=$(bashio::services "mqtt" "password")
export SUPERVISOR_MQTT_HOST=$(bashio::services "mqtt" "host")
export SUPERVISOR_MQTT_PORT=$(bashio::services "mqtt" "port")
python3 /ping_logger.py
