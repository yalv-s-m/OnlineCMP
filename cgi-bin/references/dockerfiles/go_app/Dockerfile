FROM alpine:3.14

RUN apk add --no-cache go

RUN adduser -D user && \
    chown -R user:user /home

USER user

WORKDIR /home
