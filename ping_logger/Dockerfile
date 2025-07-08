FROM python:3.11-alpine

# 1️⃣ Dodanie repozytorium community (potrzebne dla py3-paho-mqtt)
RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" \
      >> /etc/apk/repositories

# 2️⃣ Instalacja: Python, pip, bash i py3-paho-mqtt
RUN apk add --no-cache \
      python3 \
      py3-pip \
      py3-paho-mqtt \
      bash

# 3️⃣ Instalacja tylko pythonping przez pip (czysty kod Python)
RUN pip3 install --no-cache-dir pythonping

# 4️⃣ Kopiowanie skryptów
COPY ping_logger.py /ping_logger.py
COPY run.sh        /run.sh

# 5️⃣ Dodanie wykonywalnych praw do run.sh
RUN chmod +x /run.sh

# 6️⃣ Komenda startowa
CMD ["/run.sh"]
