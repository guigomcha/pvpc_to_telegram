FROM python:3.7-stretch
WORKDIR /usr/src/app
COPY . .

RUN apt-get update \
     && apt-get install build-essential make gcc -y \
     && apt-get install dpkg-dev -y \
     && apt-get install libjpeg-dev -y \
    && pip install -r requirements.txt \
    && pip install --no-cache-dir . \
    && apt-get remove -y --purge make gcc build-essential \
    && apt-get auto-remove -y \
    && rm -rf /var/lib/apt/lists/* \
    && find /usr/local/lib/python3.7 -name "*.pyc" -type f -delete

ENTRYPOINT [ "sh", "-c", "python3 -u pvpcservice/rest_manager.py" ]