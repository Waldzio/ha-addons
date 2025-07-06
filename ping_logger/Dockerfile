FROM ghcr.io/home-assistant/amd64-addon-base:14.0.3
RUN apk add --no-cache python3 py3-pip && pip3 install pythonping
COPY ping_logger.py /ping_logger.py
CMD [ "python3", "/ping_logger.py" ]
