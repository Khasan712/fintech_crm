FROM python:3.10

ENV PYTHONUNBUFFERED 1

COPY . /app
# COPY ./requirements.tx /app
WORKDIR /app
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt
# EXPOSE 8001
# CMD ["gunicorn", "--bind", ":8001", "--workers", "3", "config.wsgi"]