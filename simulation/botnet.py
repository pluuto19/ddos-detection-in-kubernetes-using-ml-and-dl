#!/usr/bin/env python3
import argparse
import time
import random
import sys
import json
import os
from datetime import datetime, timedelta

class BotnetController:
    """
    Simulates a botnet command and control server
    """
    def __init__(self):
        self.bots = [
            {
                "id": "001",
                "hostname": "attacker-01",
                "ip": "192.168.10.101",
                "status": "ONLINE",
                "last_seen": datetime.now() - timedelta(minutes=random.randint(1, 5))
            },
            {
                "id": "002",
                "hostname": "attacker-02",
                "ip": "192.168.10.102",
                "status": "ONLINE",
                "last_seen": datetime.now() - timedelta(minutes=random.randint(1, 5))
            },
            {
                "id": "003",
                "hostname": "attacker-03",
                "ip": "192.168.10.103",
                "status": "ONLINE",
                "last_seen": datetime.now() - timedelta(minutes=random.randint(1, 5))
            }
        ]
        
        self.active_attacks = []
        
    def list_bots(self):
        """List all available bots"""
        print("=== Available Bots ===")
        print("ID    | Hostname    | IP Address      | Status  | Last Seen")
        print("------+-------------+-----------------+---------+----------------")
        
        for bot in self.bots:
            last_seen = bot["last_seen"].strftime("%Y-%m-%d %H:%M:%S")
            print(f"{bot['id']}   | {bot['hostname']} | {bot['ip']}  | {bot['status']}  | {last_seen}")
            
    def start_attack(self, attack_type, target, duration, bots_list):
        """Start an attack with the specified parameters"""
        if bots_list == "all":
            selected_bots = self.bots
        else:
            bot_ids = bots_list.split(",")
            selected_bots = [bot for bot in self.bots if bot["id"] in bot_ids]
            
        if not selected_bots:
            print("[!] No valid bots selected")
            return
            
        print(f"[*] Sending attack command to {len(selected_bots)} bots")
        print(f"[*] Attack type: {attack_type}")
        print(f"[*] Target: {target}")
        print(f"[*] Duration: {duration} seconds")
        
        # Simulate command sending
        print(f"[*] Command sent successfully to {len(selected_bots)} bots")
        
        # Simulate acknowledgments
        for bot in selected_bots:
            time.sleep(random.uniform(0.2, 0.5))
            print(f"[*] Bot {bot['hostname']}: Acknowledged")
            bot["status"] = "ATTACKING"
            
        # Record the attack
        attack_start = datetime.now()
        self.active_attacks.append({
            "target": target,
            "type": attack_type,
            "start_time": attack_start,
            "duration": duration,
            "bots": [bot["hostname"] for bot in selected_bots]
        })
        
        print(f"[*] Attack started at: {attack_start.strftime('%Y-%m-%d %H:%M:%S')}")
        
    def show_status(self):
        """Show the status of active attacks and bots"""
        now = datetime.now()
        
        # Clean up finished attacks
        self.active_attacks = [
            attack for attack in self.active_attacks 
            if (now - attack["start_time"]).total_seconds() < attack["duration"]
        ]
        
        if self.active_attacks:
            print("=== Active Attacks ===")
            for attack in self.active_attacks:
                elapsed = (now - attack["start_time"]).total_seconds()
                progress = min(elapsed / attack["duration"], 1.0) * 100
                print(f"Target: {attack['target']} | Type: {attack['type']} | Progress: {int(progress)}% | Bots: {len(attack['bots'])}/{len(attack['bots'])}")
                
            print("\n=== Bot Status ===")
            for bot in self.bots:
                if bot["status"] == "ATTACKING":
                    # Generate random stats
                    packets = random.randint(200000, 250000)
                    cpu = random.randint(70, 85)
                    mem = random.randint(40, 50)
                    print(f"{bot['hostname']}: ATTACKING | Packets Sent: {packets} | CPU: {cpu}% | MEM: {mem}%")
                else:
                    print(f"{bot['hostname']}: {bot['status']}")
        else:
            print("No active attacks")
            print("\n=== Bot Status ===")
            for bot in self.bots:
                print(f"{bot['hostname']}: {bot['status']}")
                
    def stop_attack(self, target=None):
        """Stop all attacks or a specific attack"""
        if not self.active_attacks:
            print("[!] No active attacks to stop")
            return
            
        if target:
            # Stop specific attack
            matching_attacks = [a for a in self.active_attacks if a["target"] == target]
            if not matching_attacks:
                print(f"[!] No active attack against {target}")
                return
                
            for attack in matching_attacks:
                print(f"[*] Stopping attack on {attack['target']}")
                self.active_attacks.remove(attack)
                
                # Update bot status
                for bot_hostname in attack["bots"]:
                    for bot in self.bots:
                        if bot["hostname"] == bot_hostname:
                            bot["status"] = "ONLINE"
        else:
            # Stop all attacks
            print(f"[*] Stopping all attacks ({len(self.active_attacks)})")
            self.active_attacks = []
            
            # Update all bot statuses
            for bot in self.bots:
                bot["status"] = "ONLINE"
                
        print("[*] Attack(s) stopped successfully")

def main():
    parser = argparse.ArgumentParser(description="Botnet Command & Control Simulator")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List available bots")
    
    # Attack command
    attack_parser = subparsers.add_parser("attack", help="Start an attack")
    attack_parser.add_argument("--type", required=True, help="Attack type (SYN Flood, HTTP Flood, UDP Flood)")
    attack_parser.add_argument("--target", required=True, help="Target IP address or hostname")
    attack_parser.add_argument("--duration", type=int, default=30, help="Attack duration in seconds")
    attack_parser.add_argument("--bots", default="all", help="Comma-separated list of bot IDs, or 'all'")
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Show attack status")
    
    # Stop command
    stop_parser = subparsers.add_parser("stop", help="Stop an attack")
    stop_parser.add_argument("--target", help="Target IP to stop attacking (or all if not specified)")
    
    args = parser.parse_args()
    
    controller = BotnetController()
    
    if args.command == "list":
        controller.list_bots()
    elif args.command == "attack":
        controller.start_attack(args.type, args.target, args.duration, args.bots)
    elif args.command == "status":
        controller.show_status()
    elif args.command == "stop":
        controller.stop_attack(args.target)
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 