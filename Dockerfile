FROM python:3.7-slim
WORKDIR /usr/src/app
COPY . .

RUN apt-get update \
    && pip install -r requirements.txt \
    && pip install --no-cache-dir . \
    && apt-get purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/* \
    && find /usr/local/lib/python3.7 -name "*.pyc" -type f -delete

ENTRYPOINT [ "sh", "-c", "python3 -u pvpcservice/rest_manager.py" ]