FROM debian:bullseye-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    wrk ca-certificates curl iputils-ping dnsutils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY attack.sh /attack.sh
RUN chmod +x /attack.sh

ENTRYPOINT ["/attack.sh"]