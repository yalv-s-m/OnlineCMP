FROM google/dart

WORKDIR /home

ARG FILENAME

ENV name=${FILENAME}

COPY $name /home

ENTRYPOINT dart /home/$name
