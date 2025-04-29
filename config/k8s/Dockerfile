FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    iperf3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .
COPY start.sh .
RUN chmod +x start.sh

ENV HTTP_PORT=8000
ENV IPERF_PORT=5201
ENV CPU_INTENSITY=100000
ENV MEMORY_SIZE=50

EXPOSE $HTTP_PORT $IPERF_PORT

CMD ["./start.sh"]