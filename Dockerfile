# syntax=docker/dockerfile:1

FROM python:3.7-slim-buster

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD exec [ "python3", "-m", "flask", "run", "--host=0.0.0.0"]
