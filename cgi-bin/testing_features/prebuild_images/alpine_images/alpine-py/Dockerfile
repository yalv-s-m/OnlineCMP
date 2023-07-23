FROM alpine:3.14

RUN apk update && apk add --no-cache python3-dev && \
    python3 -m ensurepip && \
    pip3 install --upgrade pip && \
    rm -r /usr/lib/python*/ensurepip && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

RUN adduser -D user && \
    chown -R user:user /home

USER user

WORKDIR /home
