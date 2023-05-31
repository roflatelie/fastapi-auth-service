FROM python:3.11-alpine as builder

COPY ./ ./
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python -m pip install --upgrade pip

COPY ../requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


FROM python:3.11-alpine

RUN mkdir -p /home/app

RUN adduser --disabled-password innotter-user

ENV HOME=/home/app/web
ENV APP_HOME=/home/app/web/src
RUN mkdir $HOME
WORKDIR $HOME

RUN apk update && apk add libpq
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

COPY ./docker/entrypoint.sh .
RUN chmod +x  $HOME/entrypoint.sh

COPY src/ $APP_HOME

#USER innotter-user

ENTRYPOINT ["/home/app/web/entrypoint.sh"]
