FROM python:3.11-alpine

# 1️⃣ Dołącz repozytorium community – inaczej nie znajdziesz py3-paho-mqtt
RUN echo "https://dl-cdn.alpinelinux.org/alpine/edge/community" \
      >> /etc/apk/repositories

# 2️⃣ Zainstaluj Python, pip, bash i klienta Paho MQTT
RUN apk add --no-cache \
      python3 \
      py3-pip \
      py3-paho-mqtt \
      bash

# 3️⃣ Zainstaluj jedynie pythonping przez pip (niepotrzebne zależności C)
RUN pip3 install --no-cache-dir pythonping

# 4️⃣ Kopiuj skrypty i ustaw je jako wykonywalne
COPY ping_logger.py /ping_logger.py
COPY run.sh        /run.sh
RUN chmod +x /run.sh

# 5️⃣ Uruchom run.sh przy starcie
CMD ["/run.sh"]
