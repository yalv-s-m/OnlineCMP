FROM alpine:3.13

WORKDIR /home

RUN apk add gcc musl-dev

ARG FILENAME

ENV name=${FILENAME}

COPY $name /home

ENTRYPOINT gcc /home/$name -o /home/a.out && /home/a.out
