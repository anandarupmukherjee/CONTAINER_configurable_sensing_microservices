FROM python:3
MAINTAINER ANAND MUKHERJEE @ IfM

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ADD ./app/ /app

COPY app.py app.py
COPY config_mqtt.py config_mqtt.py
COPY controller.py controller.py

ENTRYPOINT ["python3", "controller.py"]


