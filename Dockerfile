FROM python:3.10

ENV PYTHONUNBUFFERED 1

COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt


