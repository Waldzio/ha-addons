FROM ghcr.io/home-assistant/${BUILD_ARCH}-base:latest

RUN apk add --no-cache python3 py3-pip python3-venv py3-paho-mqtt

# Stwórz własne środowisko venv i doinstaluj pythonping
RUN python3 -m venv /venv \
    && /venv/bin/pip install --no-cache-dir pythonping

COPY ping_logger.py /ping_logger.py
COPY run.sh /run.sh
RUN chmod +x /run.sh

ENTRYPOINT ["/run.sh"]
