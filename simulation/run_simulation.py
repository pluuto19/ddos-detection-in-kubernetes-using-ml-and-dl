#!/usr/bin/env python3
import os
import sys
import time
import random
import subprocess
from datetime import datetime

# Import simulator classes
from terminal_simulator import (
    K8sMasterSimulator,
    K8sWorkerSimulator,
    AttackerSimulator,
    CnCServerSimulator,
    DataAggregatorSimulator
)

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def simulate_k8s_master():
    """Simulate the Kubernetes master node"""
    clear_screen()
    master = K8sMasterSimulator()
    master.show_header()
    
    print("Starting Kubernetes master node simulation...")
    time.sleep(1)
    
    master.show_cluster_status()
    time.sleep(2)
    
    master.show_pods()
    time.sleep(2)
    
    master.show_services()
    time.sleep(2)
    
    master.show_agent_logs()
    time.sleep(2)
    
    print("\nKubernetes master simulation completed.")
    input("Press Enter to continue...")

def simulate_k8s_worker(worker_id=1, attack_type=None):
    """Simulate a Kubernetes worker node"""
    clear_screen()
    worker = K8sWorkerSimulator(f"k8s-worker-{worker_id:02d}")
    worker.show_header()
    
    print(f"Starting Kubernetes worker {worker_id} simulation...")
    time.sleep(1)
    
    worker.show_system_info()
    time.sleep(2)
    
    worker.show_network_traffic()
    time.sleep(2)
    
    worker.show_agent_status()
    time.sleep(2)
    
    if attack_type:
        worker.show_under_attack(attack_type)
        time.sleep(2)
    
    print(f"\nKubernetes worker {worker_id} simulation completed.")
    input("Press Enter to continue...")

def simulate_cnc_server(attack_type=None, target="192.168.1.100", duration=30):
    """Simulate the Command and Control server"""
    clear_screen()
    cnc = CnCServerSimulator()
    cnc.show_header()
    
    print("Starting Command and Control server simulation...")
    time.sleep(1)
    
    cnc.show_bot_list()
    time.sleep(2)
    
    if attack_type:
        cnc.issue_attack_command(attack_type, target, duration)
        time.sleep(2)
        
        cnc.show_attack_status()
        time.sleep(2)
    
    print("\nCommand and Control server simulation completed.")
    input("Press Enter to continue...")

def simulate_attacker(attacker_id=1, attack_type=None, target="192.168.1.100", duration=30):
    """Simulate an attacker node"""
    clear_screen()
    attacker = AttackerSimulator(f"attacker-{attacker_id:02d}")
    attacker.show_header()
    
    print(f"Starting attacker {attacker_id} simulation...")
    time.sleep(1)
    
    attacker.show_attack_preparation(target, attack_type)
    time.sleep(2)
    
    if attack_type:
        attacker.launch_attack(target, attack_type, duration)
        time.sleep(2)
    
    print(f"\nAttacker {attacker_id} simulation completed.")
    input("Press Enter to continue...")

def simulate_data_aggregator(attack_type=None):
    """Simulate the data aggregator"""
    clear_screen()
    aggregator = DataAggregatorSimulator()
    aggregator.show_header()
    
    print("Starting data aggregator simulation...")
    time.sleep(1)
    
    aggregator.show_status()
    time.sleep(2)
    
    aggregator.collect_data()
    time.sleep(2)
    
    aggregator.process_data()
    time.sleep(2)
    
    aggregator.run_inference()
    time.sleep(2)
    
    print("\nData aggregator simulation completed.")
    input("Press Enter to continue...")

def run_data_generator():
    """Run the data generator script for the dashboard"""
    script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                              "dashboard", "data_generator.py")
    
    if os.path.exists(script_path):
        print("Starting data generator for dashboard...")
        subprocess.Popen([sys.executable, script_path])
        time.sleep(2)
    else:
        print(f"Data generator script not found at {script_path}")

def main():
    clear_screen()
    print("=== DDoS Detection in Kubernetes Simulation ===")
    print("This script will simulate the terminals for the demo")
    print("1. K8s Master")
    print("2. K8s Worker 1")
    print("3. K8s Worker 2")
    print("4. K8s Worker 3")
    print("5. CnC Server")
    print("6. Attacker 1")
    print("7. Attacker 2")
    print("8. Attacker 3")
    print("9. Data Aggregator")
    print("10. Run Data Generator (for dashboard)")
    print("11. Run Full Attack Simulation")
    print("0. Exit")
    
    choice = input("\nEnter your choice (0-11): ")
    
    attack_types = {
        "1": "SYN Flood",
        "2": "HTTP Flood",
        "3": "UDP Flood"
    }
    
    if choice == "1":
        simulate_k8s_master()
    elif choice == "2":
        simulate_k8s_worker(1)
    elif choice == "3":
        simulate_k8s_worker(2)
    elif choice == "4":
        simulate_k8s_worker(3)
    elif choice == "5":
        attack_choice = input("Select attack type (1=SYN Flood, 2=HTTP Flood, 3=UDP Flood, 0=None): ")
        attack_type = attack_types.get(attack_choice, None)
        simulate_cnc_server(attack_type)
    elif choice == "6":
        attack_choice = input("Select attack type (1=SYN Flood, 2=HTTP Flood, 3=UDP Flood, 0=None): ")
        attack_type = attack_types.get(attack_choice, None)
        simulate_attacker(1, attack_type)
    elif choice == "7":
        attack_choice = input("Select attack type (1=SYN Flood, 2=HTTP Flood, 3=UDP Flood, 0=None): ")
        attack_type = attack_types.get(attack_choice, None)
        simulate_attacker(2, attack_type)
    elif choice == "8":
        attack_choice = input("Select attack type (1=SYN Flood, 2=HTTP Flood, 3=UDP Flood, 0=None): ")
        attack_type = attack_types.get(attack_choice, None)
        simulate_attacker(3, attack_type)
    elif choice == "9":
        simulate_data_aggregator()
    elif choice == "10":
        run_data_generator()
    elif choice == "11":
        run_full_simulation()
    elif choice == "0":
        print("Exiting...")
        sys.exit(0)
    else:
        print("Invalid choice!")
    
    # Return to main menu
    main()

def run_full_simulation():
    """Run a full attack simulation"""
    clear_screen()
    print("=== Running Full Attack Simulation ===")
    
    # Choose attack type
    print("Select attack type:")
    print("1. SYN Flood")
    print("2. HTTP Flood") 
    print("3. UDP Flood")
    attack_choice = input("Enter choice (1-3): ")
    
    attack_types = {
        "1": "SYN Flood",
        "2": "HTTP Flood",
        "3": "UDP Flood"
    }
    attack_type = attack_types.get(attack_choice, "SYN Flood")
    
    # Start data generator
    run_data_generator()
    
    # Simulate CnC server
    simulate_cnc_server(attack_type)
    
    # Simulate attackers
    for i in range(1, 4):
        simulate_attacker(i, attack_type)
    
    # Simulate workers under attack
    for i in range(1, 4):
        simulate_k8s_worker(i, attack_type)
    
    # Simulate master
    simulate_k8s_master()
    
    # Simulate data aggregator
    simulate_data_aggregator()
    
    print("\nFull simulation completed!")
    input("Press Enter to return to main menu...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0) 