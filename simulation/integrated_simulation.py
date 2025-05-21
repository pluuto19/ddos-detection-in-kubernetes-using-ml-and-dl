#!/usr/bin/env python3
import os
import sys
import time
import random
import threading
import argparse
import subprocess
from datetime import datetime

# Import our connector
from data_aggregator_connector import DataAggregatorConnector

class IntegratedSimulation:
    """
    Integrates the terminal simulations with the data aggregator connector
    to ensure data is properly sent to InfluxDB during the simulation
    """
    def __init__(self):
        self.connector = DataAggregatorConnector()
        self.attack_running = False
        self.attack_type = None
        self.attack_thread = None
        self.data_generator_process = None
        
    def start_data_generator(self):
        """Start the data generator script for the dashboard"""
        script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                  "dashboard", "data_generator.py")
        
        if os.path.exists(script_path):
            print("Starting data generator for dashboard...")
            self.data_generator_process = subprocess.Popen([sys.executable, script_path])
            return True
        else:
            print(f"Data generator script not found at {script_path}")
            return False
            
    def stop_data_generator(self):
        """Stop the data generator process"""
        if self.data_generator_process:
            print("Stopping data generator...")
            self.data_generator_process.terminate()
            self.data_generator_process = None
            
    def start_attack_simulation(self, attack_type, duration=60):
        """Start an attack simulation thread"""
        if self.attack_running:
            print("Attack simulation already running")
            return False
            
        self.attack_type = attack_type
        self.attack_running = True
        
        self.attack_thread = threading.Thread(
            target=self._run_attack_simulation,
            args=(attack_type, duration)
        )
        self.attack_thread.daemon = True
        self.attack_thread.start()
        
        return True
        
    def _run_attack_simulation(self, attack_type, duration):
        """Run the attack simulation in a separate thread"""
        print(f"\n=== Starting {attack_type} attack simulation ===")
        print(f"Duration: {duration} seconds")
        
        # Simulate pre-attack metrics
        print("\n[1/3] Sending normal metrics...")
        for i in range(5):
            for node_id in [f"k8s-worker-{j:02d}" for j in range(1, 4)]:
                self.connector.write_metrics(node_id)
                time.sleep(0.5)
                
        # Simulate attack metrics
        print("\n[2/3] Simulating attack metrics...")
        start_time = time.time()
        while time.time() - start_time < duration and self.attack_running:
            for node_id in [f"k8s-worker-{j:02d}" for j in range(1, 4)]:
                self.connector.write_metrics(node_id, attack_type, True)
                time.sleep(1)
                
        # Simulate post-attack metrics
        print("\n[3/3] Sending post-attack normal metrics...")
        for i in range(5):
            for node_id in [f"k8s-worker-{j:02d}" for j in range(1, 4)]:
                self.connector.write_metrics(node_id)
                time.sleep(0.5)
                
        print("\n=== Attack simulation completed ===")
        self.attack_running = False
        self.attack_type = None
        
    def stop_attack_simulation(self):
        """Stop the current attack simulation"""
        if not self.attack_running:
            print("No attack simulation is running")
            return False
            
        print(f"Stopping {self.attack_type} attack simulation...")
        self.attack_running = False
        
        # Wait for the thread to finish
        if self.attack_thread and self.attack_thread.is_alive():
            self.attack_thread.join(timeout=5)
            
        return True
        
    def run_terminal_simulation(self, simulation_type):
        """Run a specific terminal simulation"""
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "run_simulation.py")
        
        if not os.path.exists(script_path):
            print(f"Simulation script not found at {script_path}")
            return False
            
        # Map simulation type to choice number in run_simulation.py
        choice_map = {
            "master": "1",
            "worker1": "2",
            "worker2": "3",
            "worker3": "4",
            "cnc": "5",
            "attacker1": "6",
            "attacker2": "7",
            "attacker3": "8",
            "data-aggregator": "9",
            "full": "11"
        }
        
        if simulation_type not in choice_map:
            print(f"Unknown simulation type: {simulation_type}")
            return False
            
        # Run the simulation script with the appropriate choice
        choice = choice_map[simulation_type]
        
        # For attack simulations, also start the data flow
        if simulation_type in ["cnc", "attacker1", "attacker2", "attacker3", "full"]:
            attack_types = ["SYN Flood", "HTTP Flood", "UDP Flood"]
            attack_type = random.choice(attack_types)
            
            # Start the attack simulation in a separate thread
            self.start_attack_simulation(attack_type, 60)
            
        # Run the terminal simulation
        subprocess.run([sys.executable, script_path], input=choice.encode())
        
        return True
        
    def run_multi_terminal(self):
        """Run the multi-terminal simulator"""
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "multi_terminal_simulator.py")
        
        if not os.path.exists(script_path):
            print(f"Multi-terminal simulator script not found at {script_path}")
            return False
            
        # Start the data generator
        self.start_data_generator()
        
        # Run the multi-terminal simulator
        subprocess.run([sys.executable, script_path])
        
        # Stop the data generator
        self.stop_data_generator()
        
        return True
        
    def run_interactive(self):
        """Run the simulation in interactive mode"""
        while True:
            print("\n=== DDoS Detection in Kubernetes Simulation ===")
            print("1. Start Multi-Terminal Simulator")
            print("2. Run K8s Master Simulation")
            print("3. Run K8s Worker Simulation")
            print("4. Run CnC Server Simulation")
            print("5. Run Attacker Simulation")
            print("6. Run Data Aggregator Simulation")
            print("7. Start Data Generator")
            print("8. Start Attack Simulation")
            print("9. Stop Attack Simulation")
            print("0. Exit")
            
            choice = input("\nEnter your choice (0-9): ")
            
            if choice == "1":
                self.run_multi_terminal()
            elif choice == "2":
                self.run_terminal_simulation("master")
            elif choice == "3":
                worker_id = input("Enter worker ID (1-3): ")
                if worker_id in ["1", "2", "3"]:
                    self.run_terminal_simulation(f"worker{worker_id}")
                else:
                    print("Invalid worker ID")
            elif choice == "4":
                self.run_terminal_simulation("cnc")
            elif choice == "5":
                attacker_id = input("Enter attacker ID (1-3): ")
                if attacker_id in ["1", "2", "3"]:
                    self.run_terminal_simulation(f"attacker{attacker_id}")
                else:
                    print("Invalid attacker ID")
            elif choice == "6":
                self.run_terminal_simulation("data-aggregator")
            elif choice == "7":
                if self.data_generator_process:
                    print("Data generator is already running")
                else:
                    self.start_data_generator()
            elif choice == "8":
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
                
                if attack_choice in attack_types:
                    attack_type = attack_types[attack_choice]
                    duration = int(input("Enter duration in seconds (default: 60): ") or "60")
                    self.start_attack_simulation(attack_type, duration)
                else:
                    print("Invalid attack type")
            elif choice == "9":
                self.stop_attack_simulation()
            elif choice == "0":
                print("Exiting...")
                self.stop_data_generator()
                if self.attack_running:
                    self.stop_attack_simulation()
                break
            else:
                print("Invalid choice!")

def main():
    parser = argparse.ArgumentParser(description="Integrated DDoS Detection Simulation")
    parser.add_argument("--multi", action="store_true", help="Run multi-terminal simulator")
    parser.add_argument("--terminal", choices=["master", "worker1", "worker2", "worker3", 
                                             "cnc", "attacker1", "attacker2", "attacker3", 
                                             "data-aggregator", "full"],
                       help="Run a specific terminal simulation")
    parser.add_argument("--attack", choices=["syn_flood", "http_flood", "udp_flood"],
                       help="Simulate an attack of the specified type")
    parser.add_argument("--duration", type=int, default=60,
                       help="Duration of the attack simulation in seconds")
    parser.add_argument("--data-generator", action="store_true",
                       help="Start the data generator for the dashboard")
    
    args = parser.parse_args()
    simulation = IntegratedSimulation()
    
    try:
        if args.data_generator:
            simulation.start_data_generator()
            print("Press Ctrl+C to stop the data generator")
            while True:
                time.sleep(1)
        elif args.attack:
            attack_type = args.attack.replace("_", " ").title()
            simulation.start_attack_simulation(attack_type, args.duration)
            
            # Wait for the attack simulation to complete
            if simulation.attack_thread:
                simulation.attack_thread.join()
        elif args.multi:
            simulation.run_multi_terminal()
        elif args.terminal:
            simulation.run_terminal_simulation(args.terminal)
        else:
            simulation.run_interactive()
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        simulation.stop_data_generator()
        if simulation.attack_running:
            simulation.stop_attack_simulation()

if __name__ == "__main__":
    main() 