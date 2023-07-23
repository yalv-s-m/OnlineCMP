FROM python:3.9.6

WORKDIR /home

ARG FILENAME

ENV name=${FILENAME}  

COPY $name /home

ENTRYPOINT python3 /home/$name

