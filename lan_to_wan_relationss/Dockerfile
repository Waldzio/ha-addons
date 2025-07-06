FROM python:3.11-alpine

RUN pip install pythonping paho-mqtt

COPY lan_to_wan_relationss.py /lan_to_wan_relationss.py
CMD [ "python", "/lan_to_wan_relationss.py" ]