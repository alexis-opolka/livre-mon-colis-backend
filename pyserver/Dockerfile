FROM python:3.12.0-alpine3.18

COPY ./requirements.txt ./requirements.txt
COPY ./mongoserv/ ./mongoserv/
COPY ./.env ./.env

RUN pip3 install -r ./requirements.txt

ENTRYPOINT [ "uvicorn", "server:app", "--reload" ]
