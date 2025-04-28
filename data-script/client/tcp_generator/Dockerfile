FROM alpine:3.16

RUN apk add --no-cache iperf3

COPY attack.sh /attack.sh
RUN chmod +x /attack.sh

ENTRYPOINT ["/attack.sh"]