FROM alpine:3.14

RUN apk add --no-cache nodejs=14.21.3-r0

RUN adduser -D user && \
    chown -R user:user /home

USER user

WORKDIR /home
