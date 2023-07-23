FROM golang:1.16.3

ARG FILENAME

ENV name=${FILENAME}

WORKDIR /app

ADD $name /app 

RUN go mod init go_app

ENTRYPOINT go run $name
