FROM python:3.11-alpine

# Zainstaluj Python, pip, klienta MQTT i bash
RUN apk add --no-cache \
      python3 \
      py3-pip \
      py3-paho-mqtt \
      bash

# Zainstaluj tylko pythonping z pip (lekki, czysty)
RUN pip3 install --no-cache-dir pythonping

# Skopiuj skrypty do kontenera
COPY ping_logger.py /ping_logger.py
COPY run.sh        /run.sh

# Nadaj prawa wykonywalności dla run.sh
RUN chmod +x /run.sh

# Uruchom skrypt startowy
CMD ["/run.sh"]
