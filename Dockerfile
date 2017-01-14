FROM alpine:latest
MAINTAINER playniuniu@gmail.com

ENV BUILD_DEP="build-base python3-dev libffi-dev openssl-dev" \
    BUILD_PACKAGE="python3 sshpass openssh-client"

WORKDIR /data
COPY . /data

RUN apk add --no-cache --update $BUILD_PACKAGE $BUILD_DEP \
    && python3 -m venv /env \
    && /env/bin/pip3 install -r /data/requirments.txt \
    && apk del $BUILD_DEP \
    && rm -rf /var/cache/apk/*

VOLUME /data/file

ENTRYPOINT ["/data/command.py"]
CMD ["-h"]
