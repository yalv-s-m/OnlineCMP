FROM alpine:3.13

RUN apk add gcc musl-dev

WORKDIR /home

COPY main.c /home

RUN gcc /home/main.c -o /home/a.out
