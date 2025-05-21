# DDoS Detection in Kubernetes Simulation

This directory contains simple scripts for simulating a DDoS attack detection system in a Kubernetes environment.

## Components

- **K8s Master**: Simulates a Kubernetes master node
- **K8s Workers**: Simulates Kubernetes worker nodes (3 nodes)
- **CnC Server**: Simulates a Command and Control server that orchestrates attacks
- **Botnet**: Simulates botnet nodes (3 bots) that execute attacks
- **Data Aggregator**: Simulates the data collection and analysis system
- **Dashboard**: Displays the attack detection results

## Scripts

- `k8s_master.py`: Simulates a Kubernetes master node
- `k8s_worker.py`: Simulates a Kubernetes worker node
- `cnc_server.py`: Simulates a Command and Control server
- `botnet.py`: Simulates a botnet node
- `data_aggregator.py`: Simulates the data aggregator server
- `run_dashboard.py`: Runs the dashboard data generator

## Usage

### Running Individual Components

1. **K8s Master**:
   ```bash
   python k8s_master.py
   ```

2. **K8s Worker** (specify worker ID 1-3):
   ```bash
   python k8s_worker.py 1
   ```

3. **CnC Server**:
   ```bash
   python cnc_server.py
   ```

4. **Botnet Node** (specify bot ID 1-3):
   ```bash
   python botnet.py 1
   ```

5. **Data Aggregator**:
   ```bash
   python data_aggregator.py
   ```

6. **Dashboard**:
   ```bash
   python run_dashboard.py
   ```

## Recording with OBS

To record the simulation for demonstration:

1. Start OBS Studio
2. Add the terminal windows as sources
3. Run the simulation scripts in separate terminals
4. Record or stream as needed

## Notes

- The simulations are designed to be visually interesting for recording purposes
- CnC server accepts commands: help, list, attack, stop, status
- K8s worker and data aggregator will randomly simulate attacks
- Botnet nodes will randomly receive commands from CnC
- Dashboard data generator will store data in InfluxDB for visualization in Grafana 