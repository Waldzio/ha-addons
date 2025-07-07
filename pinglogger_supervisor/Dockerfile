FROM ghcr.io/home-assistant/amd64-addon-base:14.1.1

RUN apk add --no-cache python3 py3-pip bash
RUN pip3 install pythonping paho-mqtt

COPY ping_logger.py /ping_logger.py
COPY run.sh /run.sh
RUN chmod +x /run.sh

CMD ["/run.sh"]
