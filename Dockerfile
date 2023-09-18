ARG PYTHON_VERSION=3.10-slim-bullseye

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /code

WORKDIR /code
RUN apt-get update
RUN apt-get install build-essential -y

COPY requirements.txt requirements.txt
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    rm -rf /root/.cache/
COPY OnlineStoreDjango /code
RUN python manage.py collectstatic --no-input

RUN apt-get install htop -y
EXPOSE 8000
ENTRYPOINT ["/code/swap.sh"]

