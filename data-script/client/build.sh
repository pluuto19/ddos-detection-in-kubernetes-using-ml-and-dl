#!/bin/bash
set -e

echo "Starting HTTP attacker image build"
docker build -t fyp/http-attacker ./http_generator/
echo "Image built successfully"

echo "Starting TCP attacker image build"
docker build -t fyp/tcp-attacker ./tcp_generator/
echo "Image built successfully"