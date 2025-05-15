# Kubernetes DDoS Detection Dashboard Simulation

A local, single-node simulation of a Kubernetes DDoS Detection Dashboard using Grafana and InfluxDB. This project generates fake metric data to simulate normal traffic and DDoS attacks.

## Components

- **InfluxDB**: Time-series database to store metrics
- **Grafana**: Dashboard for visualization
- **Python Data Generator**: Script to generate and send fake metrics

## Prerequisites

- Docker and Docker Compose
- Python 3.6+
- pip (Python package installer)

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd ddos-detection-dashboard
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Dashboard

1. Start InfluxDB and Grafana with Docker Compose:
   ```bash
   docker-compose up -d
   ```

2. Wait for the services to start (approximately 30 seconds)

3. Run the metric data generator:
   ```bash
   python data_generator.py
   ```

4. Access the Grafana dashboard:
   - URL: http://localhost:3000
   - Default login: admin/admin

5. Configure InfluxDB as a data source in Grafana (if not automatically configured):
   - Go to Configuration > Data Sources > Add data source
   - Select InfluxDB
   - Set URL to http://influxdb:8086
   - Set database to ddos_demo
   - Set organization to ddos_org
   - Set token to my-super-secret-auth-token
   - Set bucket to ddos_demo

6. Import the dashboard:
   - Go to Dashboard > Import
   - Upload the `grafana_dashboard.json` file or paste its contents

## Using the Dashboard

### Dashboard Features

- **Attack Status**: Shows whether a DDoS attack is currently detected
- **Current Attack Type**: Shows the type of attack (HTTP, TCP, UDP, or none)
- **CPU Usage**: Line graph of CPU utilization
- **Memory Usage**: Line graph of memory utilization
- **Network Traffic**: Line graph showing network input/output
- **Syscall Count**: Line graph of system call frequency
- **Anomaly Score**: Gauge and line graph showing the anomaly detection score
- **Attack Type Distribution**: Pie chart showing distribution of attack types over time

### Customization Options

- **Time Range**: Adjust the time range in the top-right corner of Grafana
- **Refresh Rate**: Change the auto-refresh interval (default is 5s)
- **Panel Interactions**: Hover over graphs for details, click on legends to show/hide series

## Simulated Attack Behavior

The data generator alternates between normal and attack phases:
- **Normal Phase**: 4-8 minutes with low resource usage
- **Attack Phase**: 4-8 minutes with high resource usage
- **Attack Types**: HTTP, TCP, and UDP attacks are randomly simulated

## Stopping the Services

1. Stop the data generator with Ctrl+C
2. Stop the Docker containers:
   ```bash
   docker-compose down
   ```

## Troubleshooting

- If you don't see data in Grafana, verify that InfluxDB is properly configured as a data source
- Check that the Python script is running and successfully connecting to InfluxDB
- Verify that the dashboard is imported correctly
- Look at Docker logs for any errors:
  ```bash
  docker-compose logs
  ``` 