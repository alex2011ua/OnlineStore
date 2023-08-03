ARG PYTHON_VERSION=3.10-slim-bullseye

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /code

COPY requirements.txt requirements.txt
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    rm -rf /root/.cache/
COPY OnlineStoreDjango /code
RUN python manage.py collectstatic --no-input


EXPOSE 8000
CMD ["gunicorn", "OnlineStoreDjango.wsgi:application","--bind", "0.0.0.0:8000"]
