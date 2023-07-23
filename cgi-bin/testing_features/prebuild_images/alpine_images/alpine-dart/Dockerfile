FROM alpine:3.14

RUN apk add --no-cache curl bash

RUN curl --location --fail --show-error https://storage.googleapis.com/dart-archive/channels/stable/release/3.0.5/sdk/dartsdk-linux-x64-release.zip -o /tmp/dartsdk.zip \
    && unzip /tmp/dartsdk.zip -d /usr/local \
    && rm /tmp/dartsdk.zip

ENV PATH="/usr/local/dart-sdk/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

RUN adduser -D user \
    && chown -R user:user /home

USER user

WORKDIR /home
