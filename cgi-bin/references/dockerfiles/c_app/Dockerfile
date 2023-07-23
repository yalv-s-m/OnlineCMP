FROM alpine:3.13

RUN apk add gcc musl-dev

WORKDIR /home

COPY main.c /home

ENTRYPOINT gcc /home/main.c -o /home/a.out && /home/a.out
