FROM python:3.10-alpine



WORKDIR /app

COPY ./app/requirements.txt .

RUN pip install -r requirements.txt

COPY ./app .
