FROM swift:5.7.3-focal

WORKDIR /home

ARG FILENAME

ENV name=${FILENAME}

COPY $name /home

ENTRYPOINT swift /home/$name
