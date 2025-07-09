FROM python:3.11-slim

RUN apt-get update \
 && apt-get install -y bash python3-paho-mqtt \
 && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pythonping

COPY ping_logger.py /ping_logger.py
COPY run.sh        /run.sh
RUN chmod +x /run.sh

CMD ["/run.sh"]
