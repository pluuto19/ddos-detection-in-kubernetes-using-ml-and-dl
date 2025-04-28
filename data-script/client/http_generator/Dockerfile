FROM alpine:3.16

RUN apk add --no-cache build-base openssl-dev git zlib-dev \
    && git clone https://github.com/wg/wrk.git \
    && cd wrk \
    && make \
    && cp wrk /usr/local/bin \
    && cd .. \
    && rm -rf wrk \
    && apk del git build-base

COPY attack.sh /attack.sh
RUN chmod +x /attack.sh

ENTRYPOINT ["/attack.sh"]