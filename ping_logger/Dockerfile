FROM ghcr.io/home-assistant/${BUILD_ARCH}-base:latest

# Zainstaluj Python i MQTT (Alpine)
RUN apk add --no-cache python3 py3-pip py3-paho-mqtt

# Pozwól pipowi nadpisać systemowe pakiety
RUN pip install --break-system-packages pythonping

COPY ping_logger.py /ping_logger.py
COPY run.sh /run.sh
RUN chmod +x /run.sh

CMD ["/run.sh"]
