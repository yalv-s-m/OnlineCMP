FROM gcc:9.4.0

WORKDIR /home

ARG FILENAME

ENV name=${FILENAME}

COPY $name /home

ENTRYPOINT g++ /home/$name -o /home/a.out && /home/a.out
