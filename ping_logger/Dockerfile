FROM python:3.11-alpine

# Zainstaluj Python i pip, a także bash (dla run.sh)
RUN apk add --no-cache python3 py3-pip bash

# Zainstaluj zależności Pythona
RUN pip3 install pythonping paho-mqtt

# Skopiuj skrypty
COPY ping_logger.py /ping_logger.py
COPY run.sh /run.sh

# Nadaj prawa wykonywalności
RUN chmod +x /run.sh

# Uruchom skrypt przez run.sh (bashio do pobrania poświadczeń)
CMD ["/run.sh"]
