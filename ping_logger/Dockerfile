ARG BUILD_FROM
FROM $BUILD_FROM

ARG BUILD_ARCH
ENV LANG C.UTF-8

# Dodaj klienta MQTT w Alpine
RUN apk add --no-cache python3 py3-pip py3-paho-mqtt

# Zainstaluj pythonping
RUN pip3 install --no-cache-dir pythonping

COPY run.sh /run.sh
COPY ping_logger.py /ping_logger.py
RUN chmod +x /run.sh

CMD ["/run.sh"]
