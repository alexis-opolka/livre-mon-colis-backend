FROM python:3.9.18-alpine3.18

COPY ./requirements.txt ./requirements.txt
COPY ./mongo_server.py ./mongo_server.py
COPY ./.env ./.env

RUN pip3 install -r ./requirements.txt

ENTRYPOINT [ "python", "/mongo_server.py" ]