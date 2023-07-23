FROM alpine:3.13

RUN apk add gcc musl-dev

COPY file.c /

ENTRYPOINT gcc file.c -o a.out && ./a.out

