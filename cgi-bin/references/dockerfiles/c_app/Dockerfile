FROM alpine:3.14

RUN apk add --no-cache gcc musl-dev

RUN adduser -D user && \
    chown -R user:user /home

USER user

WORKDIR /home
