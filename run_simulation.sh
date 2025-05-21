#!/bin/bash

echo "DDoS Detection in Kubernetes Simulation"
echo "====================================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed or not in the PATH."
    echo "Please install Python 3.6+ and try again."
    exit 1
fi

# Check if required packages are installed
echo "Checking required packages..."
if ! python3 -c "import influxdb_client" &> /dev/null; then
    echo "Installing required packages..."
    pip3 install influxdb-client
fi

echo
echo "Starting the simulation..."
echo
cd simulation
python3 integrated_simulation.py 