#!/bin/sh

THREADS=2
CONNECTIONS=10
DURATION=60
TARGET="http://localhost:80"

while [ "$#" -gt 0 ]; do
  case "$1" in
    -t|--threads) THREADS="$2"; shift 2 ;;
    -c|--connections) CONNECTIONS="$2"; shift 2 ;;
    -d|--duration) DURATION="$2"; shift 2 ;;
    -*) echo "Unknown option: $1" >&2; exit 1 ;;
    *) TARGET="$1"; shift ;;
  esac
done

echo "Starting HTTP attack against $TARGET"
echo "Threads: $THREADS, Connections: $CONNECTIONS, Duration: $DURATION seconds"

exec wrk -t"$THREADS" -c"$CONNECTIONS" -d"${DURATION}s" --latency "$TARGET"