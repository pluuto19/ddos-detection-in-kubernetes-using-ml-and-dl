i# Kubernetes DoS Detection System Demo Simulator

This directory contains scripts to simulate a Kubernetes DoS detection system for demonstration purposes. The simulation creates multiple terminal windows representing different components of the system and orchestrates a simulated attack scenario.

## Components Simulated

1. **Kubernetes Master Node** - Shows cluster status, pods, and services
2. **Kubernetes Worker Nodes** (3) - Shows system metrics and agent status
3. **Attacker Nodes** (3) - Simulates attack execution
4. **Command and Control Server** - Controls the attacker nodes
5. **Data Aggregator** - Collects metrics and runs inference
6. **Dashboard** - Visualizes system status and attack detection

## Requirements

- Python 3.6+
- Terminal emulator (gnome-terminal, xterm, or Terminal.app on macOS)
- curses library (usually included with Python)

## Setup

1. Make sure all scripts are executable:

```bash
chmod +x *.py
```

2. Install required Python packages:

```bash
pip install argparse
```

## Running the Demo

### Option 1: Full Demo

To run the complete demo with all components and the attack scenario:

```bash
./demo_orchestrator.py
```

This will:
1. Launch all terminal windows
2. Wait for them to initialize
3. Start the attack scenario
4. Show the attack detection in the dashboard

### Option 2: Just Launch Terminals

To only launch the terminal windows without running the attack scenario:

```bash
./demo_orchestrator.py --launch
```

### Option 3: Run Attack Scenario

If you've already launched the terminals and want to run the attack scenario:

```bash
./demo_orchestrator.py --attack
```

## Dashboard Controls

The dashboard UI has the following keyboard controls:

- `a` - Simulate an attack
- `s` - Stop the simulated attack
- `q` - Quit the dashboard

## Individual Components

You can also run each component individually:

- **Terminal Simulator**: `./terminal_simulator.py`
- **Dashboard UI**: `./dashboard_ui.py`
- **Attack Script**: `./attack.py --type syn_flood --target 192.168.1.100 --duration 30`
- **Botnet Control**: `./botnet.py list`
- **Data Aggregator**: `./data_aggregator_sim.py --status`

## Recording with OBS

To record the demo with OBS:

1. Set up OBS to capture specific windows or regions of your screen
2. Arrange the terminal windows in a logical layout
3. Consider using different backgrounds or terminal colors to visually differentiate the components
4. Start recording in OBS and then run the demo

## Customization

You can customize the demo by:

- Modifying the terminal positions in `demo_orchestrator.py`
- Changing the attack types in `attack.py`
- Adjusting the dashboard visualization in `dashboard_ui.py`
- Adding more commands to the terminal simulators

## Troubleshooting

- If terminals don't open, check if you have gnome-terminal or xterm installed
- If the dashboard doesn't display correctly, try resizing the terminal window
- If scripts fail to run, ensure they have executable permissions

## License

This simulation is provided for educational purposes only. 