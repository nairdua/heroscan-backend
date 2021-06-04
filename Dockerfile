FROM python:3.7-slim-buster as builder

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.7-slim-buster

RUN apt-get update && apt-get install -y python3-opencv

COPY . .
COPY --from=builder /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"
EXPOSE 8000
CMD ["gunicorn", "main:app", "-w 2", "--worker-class=gthread", "-b 0.0.0.0:8000"]
