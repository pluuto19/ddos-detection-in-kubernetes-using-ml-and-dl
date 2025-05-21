#!/usr/bin/env python3
import os
import time
import random
import sys
from datetime import datetime

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the terminal header"""
    print("=" * 60)
    print("COMMAND AND CONTROL SERVER (cnc-server)")
    print("=" * 60)
    print()

def simulate_cnc_server():
    """Simulate a Command and Control server"""
    clear_screen()
    print_header()
    
    # Bot information
    bots = [
        {"id": "001", "hostname": "attacker-01", "ip": "192.168.10.101", "status": "ONLINE"},
        {"id": "002", "hostname": "attacker-02", "ip": "192.168.10.102", "status": "ONLINE"},
        {"id": "003", "hostname": "attacker-03", "ip": "192.168.10.103", "status": "ONLINE"}
    ]
    
    # Attack state
    attack_running = False
    attack_type = None
    attack_target = None
    attack_start_time = None
    attack_duration = 0
    
    print("[*] CnC Server initialized")
    print("[*] Connected to botnet")
    print("[*] Type 'help' for available commands")
    
    while True:
        try:
            current_time = datetime.now()
            
            # If attack is running, check if it should end
            if attack_running and (current_time - attack_start_time).total_seconds() > attack_duration:
                print(f"\n[{current_time.strftime('%H:%M:%S')}] Attack completed")
                print(f"[{current_time.strftime('%H:%M:%S')}] Sending stop command to all bots")
                
                for bot in bots:
                    time.sleep(0.5)
                    print(f"[{current_time.strftime('%H:%M:%S')}] Bot {bot['hostname']} acknowledged stop command")
                    bot["status"] = "ONLINE"
                
                attack_running = False
                attack_type = None
                attack_target = None
            
            # Command prompt
            cmd = input("\ncnc> ").strip().lower()
            
            if cmd == "help":
                print("\nAvailable commands:")
                print("  list              - List all available bots")
                print("  attack            - Start an attack")
                print("  stop              - Stop ongoing attack")
                print("  status            - Show attack status")
                print("  exit/quit         - Exit the simulation")
            
            elif cmd == "list":
                print("\n=== Available Bots ===")
                print("ID    | Hostname    | IP Address      | Status")
                print("------+-------------+-----------------+--------")
                
                for bot in bots:
                    print(f"{bot['id']}   | {bot['hostname']} | {bot['ip']}  | {bot['status']}")
            
            elif cmd == "attack":
                if attack_running:
                    print("\n[!] Attack already in progress. Stop it first.")
                    continue
                
                print("\nSelect attack type:")
                print("1. SYN Flood")
                print("2. HTTP Flood")
                print("3. UDP Flood")
                
                attack_choice = input("Enter choice (1-3): ")
                attack_types = {"1": "SYN Flood", "2": "HTTP Flood", "3": "UDP Flood"}
                
                if attack_choice not in attack_types:
                    print("\n[!] Invalid attack type")
                    continue
                
                attack_type = attack_types[attack_choice]
                attack_target = "192.168.1.100"  # Default target
                
                target_input = input(f"Enter target IP [default: {attack_target}]: ")
                if target_input.strip():
                    attack_target = target_input
                
                duration_input = input("Enter attack duration in seconds [default: 30]: ")
                try:
                    attack_duration = int(duration_input) if duration_input.strip() else 30
                except ValueError:
                    attack_duration = 30
                
                print(f"\n[{current_time.strftime('%H:%M:%S')}] Starting {attack_type} attack against {attack_target}")
                print(f"[{current_time.strftime('%H:%M:%S')}] Attack duration: {attack_duration} seconds")
                print(f"[{current_time.strftime('%H:%M:%S')}] Sending commands to all bots...")
                
                attack_running = True
                attack_start_time = current_time
                
                for bot in bots:
                    time.sleep(0.5)
                    print(f"[{current_time.strftime('%H:%M:%S')}] Bot {bot['hostname']} acknowledged attack command")
                    bot["status"] = "ATTACKING"
            
            elif cmd == "stop":
                if not attack_running:
                    print("\n[!] No attack is currently running")
                    continue
                
                print(f"\n[{current_time.strftime('%H:%M:%S')}] Stopping {attack_type} attack")
                print(f"[{current_time.strftime('%H:%M:%S')}] Sending stop command to all bots")
                
                for bot in bots:
                    time.sleep(0.5)
                    print(f"[{current_time.strftime('%H:%M:%S')}] Bot {bot['hostname']} acknowledged stop command")
                    bot["status"] = "ONLINE"
                
                attack_running = False
                attack_type = None
                attack_target = None
            
            elif cmd == "status":
                if attack_running:
                    elapsed = (current_time - attack_start_time).total_seconds()
                    remaining = max(0, attack_duration - elapsed)
                    progress = min(100, (elapsed / attack_duration) * 100)
                    
                    print("\n=== Active Attack ===")
                    print(f"Type:       {attack_type}")
                    print(f"Target:     {attack_target}")
                    print(f"Progress:   {progress:.1f}%")
                    print(f"Remaining:  {remaining:.1f} seconds")
                    print(f"Bots:       {sum(1 for bot in bots if bot['status'] == 'ATTACKING')}/3")
                    
                    print("\n=== Bot Status ===")
                    for bot in bots:
                        if bot["status"] == "ATTACKING":
                            packets = random.randint(10000, 50000)
                            print(f"{bot['hostname']}: ATTACKING | Packets: {packets} | CPU: {random.randint(70, 90)}%")
                        else:
                            print(f"{bot['hostname']}: {bot['status']}")
                else:
                    print("\nNo active attacks")
                    
                    print("\n=== Bot Status ===")
                    for bot in bots:
                        print(f"{bot['hostname']}: {bot['status']}")
            
            elif cmd in ["exit", "quit"]:
                print("\nExiting CnC server simulation...")
                break
            
            else:
                print("\n[!] Unknown command. Type 'help' for available commands")
        
        except KeyboardInterrupt:
            print("\nExiting CnC server simulation...")
            break

if __name__ == "__main__":
    simulate_cnc_server() 