FROM alpine:3.14

RUN apk add --no-cache g++

RUN adduser -D user && \
    chown -R user:user /home

USER user

WORKDIR /home
