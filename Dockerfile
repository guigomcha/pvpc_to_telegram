FROM python:3.7-slim

COPY . .

RUN pip install -r requirements.txt
RUN pip install .

ENTRYPOINT [ "sh", "-c", "python3 -u pvpcservice/rest_manager.py" ]
