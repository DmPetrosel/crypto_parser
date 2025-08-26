FROM python:3.11-slim

RUN apt-get update && apt-get install -y gcc && apt-get install redis

WORKDIR /basebot_app

COPY . .
ENV PYTHONPATH=/basebot_app

RUN pip install --upgrade pip && pip install --no-cache-dir . -U


ENTRYPOINT ["run_bot"]