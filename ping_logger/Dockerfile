# Użyj oficjalnego HA base image, który zawiera Bashio:
ARG BUILD_FROM=ghcr.io/home-assistant/amd64-addon-base:stable
FROM ${BUILD_FROM}

# Zainstaluj Python i pip
RUN apk add --no-cache python3 py3-pip

# Zainstaluj zależności Pythona
RUN pip3 install pythonping paho-mqtt

# Skopiuj skrypty
COPY ping_logger.py /ping_logger.py
COPY run.sh /run.sh

# Nadaj prawa wykonywalności
RUN chmod +x /run.sh

CMD [ "/run.sh" ]
