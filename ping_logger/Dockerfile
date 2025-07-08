ARG BUILD_FROM=ghcr.io/home-assistant/amd64-addon-base:stable

FROM ${BUILD_FROM}

RUN apk add --no-cache python3 py3-pip

# Instalacja potrzebnych bibliotek
RUN pip3 install --no-cache-dir pythonping paho-mqtt

COPY ping_logger.py /ping_logger.py
COPY run.sh /run.sh

RUN chmod +x /run.sh

CMD ["/run.sh"]
