FROM python:3.11-alpine

RUN apk add --no-cache python3 py3-paho-mqtt bash

RUN pip3 install --no-cache-dir pythonping

COPY ping_logger.py /ping_logger.py
COPY run.sh        /run.sh
RUN chmod +x /run.sh

CMD ["/run.sh"]
