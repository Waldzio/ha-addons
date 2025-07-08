FROM python:3.11-alpine

# Zainstaluj python, pip, bash
RUN apk add --no-cache python3 py3-pip bash

# Zainstaluj zależności Pythonowe przez pip — to jest zawsze niezawodne!
RUN pip3 install --no-cache-dir pythonping paho-mqtt

COPY ping_logger.py /ping_logger.py
COPY run.sh        /run.sh
RUN chmod +x /run.sh

CMD ["/run.sh"]FROM python:3.11-alpine

# Zainstaluj python, pip, bash
RUN apk add --no-cache python3 py3-pip bash

# Zainstaluj zależności Pythonowe przez pip — to jest zawsze niezawodne!
RUN pip3 install --no-cache-dir pythonping paho-mqtt

COPY ping_logger.py /ping_logger.py
COPY run.sh        /run.sh
RUN chmod +x /run.sh

CMD ["/run.sh"]
