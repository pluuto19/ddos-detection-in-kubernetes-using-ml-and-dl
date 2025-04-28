#!/bin/sh

DURATION=60
PORT=5001
HOST="localhost"

while [ "$#" -gt 0 ]; do
  case "$1" in
    -t|--duration) DURATION="$2"; shift 2 ;;
    -p|--port) PORT="$2"; shift 2 ;;
    -*) echo "Unknown option: $1" >&2; exit 1 ;;
    *) HOST="$1"; shift ;;
  esac
done

echo "Starting TCP attack against $HOST:$PORT"
echo "Duration: $DURATION seconds"

exec iperf3 -c "$HOST" -p "$PORT" -t "$DURATION" -P 10 -b 0