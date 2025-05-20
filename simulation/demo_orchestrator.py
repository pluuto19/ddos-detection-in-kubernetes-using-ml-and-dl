#!/usr/bin/env python3
import os
import sys
import time
import random
import subprocess
import argparse
from datetime import datetime

# Import our simulator classes
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from terminal_simulator import (
    K8sMasterSimulator, 
    K8sWorkerSimulator,
    AttackerSimulator,
    CnCServerSimulator,
    DataAggregatorSimulator,
    DashboardSimulator
)

class DemoOrchestrator:
    """
    Orchestrates the demo by launching multiple terminal windows
    and simulating the attack scenario
    """
    def __init__(self):
        self.terminals = {}
        self.dashboard_process = None
        
    def launch_terminal(self, name, title, command, geometry="80x24+0+0"):
        """
        Launch a new terminal window with the given title and command
        """
        # Different terminal commands for different systems
        if sys.platform == "linux" or sys.platform == "linux2":
            # For Linux, use gnome-terminal or xterm
            try:
                process = subprocess.Popen([
                    "gnome-terminal",
                    "--title", title,
                    "--geometry", geometry,
                    "--", "bash", "-c", command
                ])
                return process
            except FileNotFoundError:
                try:
                    process = subprocess.Popen([
                        "xterm",
                        "-title", title,
                        "-geometry", geometry,
                        "-e", command
                    ])
                    return process
                except FileNotFoundError:
                    print(f"Could not launch terminal for {name}. Please install gnome-terminal or xterm.")
                    return None
        elif sys.platform == "darwin":
            # For macOS, use Terminal.app
            osascript_command = f'''
            tell application "Terminal"
                do script "{command}"
                set custom title of front window to "{title}"
                set bounds of front window to {{100, 100, 800, 600}}
            end tell
            '''
            process = subprocess.Popen(["osascript", "-e", osascript_command])
            return process
        else:
            print(f"Unsupported platform: {sys.platform}")
            return None
            
    def create_terminal_script(self, name, simulator_class, hostname, commands):
        """
        Create a temporary script that will run the terminal simulator
        with the specified commands
        """
        script_path = f"/tmp/terminal_{name}.py"
        with open(script_path, "w") as f:
            f.write(f"""#!/usr/bin/env python3
import os
import sys
import time
from datetime import datetime

# Add the simulation directory to the path
sys.path.append("{os.path.dirname(os.path.abspath(__file__))}")
from terminal_simulator import {simulator_class.__name__}

# Create the simulator
simulator = {simulator_class.__name__}("{hostname}")
simulator.clear_screen()
simulator.show_header()

# Run the commands
""")
            
            for cmd, delay in commands:
                f.write(f"time.sleep({delay})\n")
                f.write(f"simulator.{cmd}\n")
                
            # Keep the terminal open
            f.write("""
# Wait for user to press Enter to exit
input("\\nPress Enter to exit...")
""")
            
        os.chmod(script_path, 0o755)
        return script_path
        
    def launch_master_node(self, position="0x0"):
        """Launch the Kubernetes master node terminal"""
        commands = [
            ("show_cluster_status()", 1),
            ("show_pods()", 3),
            ("show_services()", 2),
            ("show_agent_logs()", 5)
        ]
        
        script = self.create_terminal_script(
            "master", 
            K8sMasterSimulator, 
            "k8s-master-01", 
            commands
        )
        
        process = self.launch_terminal(
            "master",
            "Kubernetes Master Node",
            f"python3 {script}",
            f"100x30+{position}"
        )
        
        self.terminals["master"] = process
        return process
        
    def launch_worker_node(self, number, position="0x0"):
        """Launch a Kubernetes worker node terminal"""
        hostname = f"k8s-worker-{number:02d}"
        
        commands = [
            ("show_system_info()", 1),
            ("show_network_traffic()", 3),
            ("show_agent_status()", 2)
        ]
        
        script = self.create_terminal_script(
            f"worker{number}", 
            K8sWorkerSimulator, 
            hostname, 
            commands
        )
        
        process = self.launch_terminal(
            f"worker{number}",
            f"Kubernetes Worker Node {number}",
            f"python3 {script}",
            f"100x30+{position}"
        )
        
        self.terminals[f"worker{number}"] = process
        return process
        
    def launch_attacker_node(self, number, position="0x0"):
        """Launch an attacker node terminal"""
        hostname = f"attacker-{number:02d}"
        
        commands = [
            (f"show_attack_preparation(target='192.168.1.100', attack_type='SYN Flood')", 1)
        ]
        
        script = self.create_terminal_script(
            f"attacker{number}", 
            AttackerSimulator, 
            hostname, 
            commands
        )
        
        process = self.launch_terminal(
            f"attacker{number}",
            f"Attacker Node {number}",
            f"python3 {script}",
            f"100x30+{position}"
        )
        
        self.terminals[f"attacker{number}"] = process
        return process
        
    def launch_cnc_server(self, position="0x0"):
        """Launch the Command and Control server terminal"""
        commands = [
            ("show_bot_list()", 1)
        ]
        
        script = self.create_terminal_script(
            "cnc", 
            CnCServerSimulator, 
            "cnc-server", 
            commands
        )
        
        process = self.launch_terminal(
            "cnc",
            "Command and Control Server",
            f"python3 {script}",
            f"100x30+{position}"
        )
        
        self.terminals["cnc"] = process
        return process
        
    def launch_data_aggregator(self, position="0x0"):
        """Launch the data aggregator terminal"""
        commands = [
            ("show_data_collection()", 1)
        ]
        
        script = self.create_terminal_script(
            "data_aggregator", 
            DataAggregatorSimulator, 
            "data-aggregator", 
            commands
        )
        
        process = self.launch_terminal(
            "data_aggregator",
            "Data Aggregator Server",
            f"python3 {script}",
            f"100x30+{position}"
        )
        
        self.terminals["data_aggregator"] = process
        return process
        
    def launch_dashboard(self, position="0x0"):
        """Launch the dashboard UI"""
        dashboard_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard_ui.py")
        
        process = self.launch_terminal(
            "dashboard",
            "DoS Detection Dashboard",
            f"python3 {dashboard_path}",
            f"120x40+{position}"
        )
        
        self.dashboard_process = process
        return process
        
    def launch_all_terminals(self):
        """Launch all terminals with appropriate positioning"""
        # Launch terminals in a grid layout
        # First row
        self.launch_master_node("0x0")
        self.launch_worker_node(1, "700x0")
        
        # Second row
        self.launch_worker_node(2, "0x400")
        self.launch_worker_node(3, "700x400")
        
        # Third row
        self.launch_cnc_server("0x800")
        self.launch_attacker_node(1, "700x800")
        
        # Fourth row
        self.launch_data_aggregator("0x1200")
        
        # Dashboard in a larger window
        self.launch_dashboard("1400x0")
        
        print("All terminals launched. Press Ctrl+C to exit.")
        
    def run_attack_scenario(self):
        """Run the attack scenario"""
        # Wait for all terminals to initialize
        print("Waiting for terminals to initialize...")
        time.sleep(5)
        
        # Update CnC server to show attack command
        print("Simulating attack command from CnC server...")
        cnc_script = self.create_terminal_script(
            "cnc_attack", 
            CnCServerSimulator, 
            "cnc-server", 
            [
                ("show_bot_list()", 1),
                ("issue_attack_command(attack_type='SYN Flood', target='192.168.1.100', duration=30)", 2),
                ("show_attack_status()", 5)
            ]
        )
        
        self.launch_terminal(
            "cnc_attack",
            "Command and Control Server (Attack)",
            f"python3 {cnc_script}",
            "100x30+0x800"
        )
        
        # Update attacker nodes to show attack execution
        for i in range(1, 4):
            attacker_script = self.create_terminal_script(
                f"attacker{i}_attack", 
                AttackerSimulator, 
                f"attacker-{i:02d}", 
                [
                    (f"show_attack_preparation(target='192.168.1.100', attack_type='SYN Flood')", 1),
                    (f"launch_attack(target='192.168.1.100', attack_type='SYN Flood', duration=30)", 2)
                ]
            )
            
            self.launch_terminal(
                f"attacker{i}_attack",
                f"Attacker Node {i} (Attack)",
                f"python3 {attacker_script}",
                f"100x30+{700*(i-1)}x800"
            )
            
        # Wait a bit for the attack to start
        time.sleep(5)
        
        # Update worker node to show it's under attack
        worker2_script = self.create_terminal_script(
            "worker2_attack", 
            K8sWorkerSimulator, 
            "k8s-worker-02", 
            [
                ("show_system_info()", 1),
                ("show_network_traffic()", 2),
                ("show_under_attack(attack_type='SYN Flood')", 3),
                ("show_agent_status()", 2)
            ]
        )
        
        self.launch_terminal(
            "worker2_attack",
            "Kubernetes Worker Node 2 (Under Attack)",
            f"python3 {worker2_script}",
            "100x30+0x400"
        )
        
        # Update data aggregator to show detection
        data_agg_script = self.create_terminal_script(
            "data_aggregator_detect", 
            DataAggregatorSimulator, 
            "data-aggregator", 
            [
                ("show_data_collection()", 1),
                ("show_data_processing()", 3),
                ("show_model_inference()", 2)
            ]
        )
        
        self.launch_terminal(
            "data_aggregator_detect",
            "Data Aggregator Server (Detection)",
            f"python3 {data_agg_script}",
            "100x30+0x1200"
        )
        
        # Trigger attack on dashboard
        # This is done by the user pressing 'a' in the dashboard UI
        print("\nPlease press 'a' in the dashboard window to simulate the attack detection.")
        
    def cleanup(self):
        """Clean up temporary files and processes"""
        # Clean up temporary scripts
        for name in ["master", "worker1", "worker2", "worker3", 
                    "attacker1", "attacker2", "attacker3", 
                    "cnc", "data_aggregator", 
                    "cnc_attack", "attacker1_attack", "attacker2_attack", 
                    "attacker3_attack", "worker2_attack", "data_aggregator_detect"]:
            script_path = f"/tmp/terminal_{name}.py"
            if os.path.exists(script_path):
                os.remove(script_path)

def main():
    parser = argparse.ArgumentParser(description="Demo orchestrator for K8s DoS detection system")
    parser.add_argument("--launch", action="store_true", help="Launch all terminal windows")
    parser.add_argument("--attack", action="store_true", help="Run the attack scenario")
    args = parser.parse_args()
    
    orchestrator = DemoOrchestrator()
    
    try:
        if args.launch:
            orchestrator.launch_all_terminals()
            
        if args.attack:
            orchestrator.run_attack_scenario()
            
        if not args.launch and not args.attack:
            # Default: launch all and run attack
            orchestrator.launch_all_terminals()
            time.sleep(5)  # Wait for terminals to initialize
            orchestrator.run_attack_scenario()
            
        # Keep running until user interrupts
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nExiting...")
        orchestrator.cleanup()

if __name__ == "__main__":
    main() 