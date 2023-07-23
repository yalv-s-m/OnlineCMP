FROM node:10.19.0

ARG FILENAME

ENV name=${FILENAME}

COPY $name /

ENTRYPOINT node $name
