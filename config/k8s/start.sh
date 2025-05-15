#!/bin/bash
set -e

echo "Starting iperf3 server on port $IPERF_PORT..."
iperf3 -s -p $IPERF_PORT &

echo "Starting HTTP server on port $HTTP_PORT..."
python server.py