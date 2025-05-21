#!/usr/bin/env python3
import os
import time
import random
import sys
from datetime import datetime

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(bot_id=1):
    """Print the terminal header"""
    hostname = f"attacker-{bot_id:02d}"
    print("=" * 60)
    print(f"BOTNET NODE ({hostname})")
    print("=" * 60)
    print()

def print_progress_bar(progress, width=50):
    """Print a progress bar"""
    filled_width = int(width * progress)
    bar = '█' * filled_width + '░' * (width - filled_width)
    print(f"[{bar}] {progress*100:.1f}%")

def simulate_botnet(bot_id=1):
    """Simulate a botnet node"""
    clear_screen()
    print_header(bot_id)
    
    # Bot state
    hostname = f"attacker-{bot_id:02d}"
    ip_address = f"192.168.10.{100 + bot_id}"
    cnc_server = "192.168.10.1"
    status = "IDLE"
    attack_type = None
    attack_target = None
    attack_start_time = None
    attack_duration = 0
    
    print(f"[*] Bot initialized: {hostname} ({ip_address})")
    print(f"[*] Connecting to CnC server at {cnc_server}...")
    time.sleep(1)
    print(f"[*] Connected to CnC server")
    print(f"[*] Waiting for commands...")
    
    # Main loop
    while True:
        try:
            current_time = datetime.now()
            
            # Simulate receiving commands from CnC
            if status == "IDLE" and random.random() < 0.05:  # 5% chance to receive attack command
                attack_types = ["SYN Flood", "HTTP Flood", "UDP Flood"]
                attack_type = random.choice(attack_types)
                attack_target = "192.168.1.100"
                attack_duration = random.randint(20, 40)
                status = "ATTACKING"
                attack_start_time = current_time
                
                print(f"\n[{current_time.strftime('%H:%M:%S')}] Received command from CnC server")
                print(f"[{current_time.strftime('%H:%M:%S')}] Attack type: {attack_type}")
                print(f"[{current_time.strftime('%H:%M:%S')}] Target: {attack_target}")
                print(f"[{current_time.strftime('%H:%M:%S')}] Duration: {attack_duration} seconds")
                print(f"[{current_time.strftime('%H:%M:%S')}] Starting attack...")
            
            # If attack is running, check if it should end
            if status == "ATTACKING" and (current_time - attack_start_time).total_seconds() > attack_duration:
                print(f"\n[{current_time.strftime('%H:%M:%S')}] Attack completed")
                print(f"[{current_time.strftime('%H:%M:%S')}] Returning to idle state")
                status = "IDLE"
                attack_type = None
                attack_target = None
            
            # Display current status
            print(f"\n[{current_time.strftime('%H:%M:%S')}] Status: {status}")
            
            if status == "ATTACKING":
                elapsed = (current_time - attack_start_time).total_seconds()
                progress = min(1.0, elapsed / attack_duration)
                
                print(f"Attack type: {attack_type}")
                print(f"Target: {attack_target}")
                print(f"Progress: ")
                print_progress_bar(progress)
                
                # Show attack-specific stats
                if attack_type == "SYN Flood":
                    packets_sent = int(progress * random.randint(100000, 500000))
                    print(f"SYN packets sent: {packets_sent}")
                    print(f"Rate: {random.randint(5000, 15000)} packets/sec")
                elif attack_type == "HTTP Flood":
                    requests_sent = int(progress * random.randint(50000, 200000))
                    print(f"HTTP requests sent: {requests_sent}")
                    print(f"Rate: {random.randint(2000, 8000)} requests/sec")
                elif attack_type == "UDP Flood":
                    packets_sent = int(progress * random.randint(150000, 600000))
                    print(f"UDP packets sent: {packets_sent}")
                    print(f"Rate: {random.randint(8000, 20000)} packets/sec")
                
                print(f"CPU usage: {random.randint(70, 95)}%")
                print(f"Memory usage: {random.randint(60, 85)}%")
                print(f"Network usage: {random.randint(70, 95)}%")
            else:
                print("Waiting for commands from CnC server...")
                print(f"CPU usage: {random.randint(5, 15)}%")
                print(f"Memory usage: {random.randint(10, 30)}%")
                print(f"Network usage: {random.randint(1, 10)}%")
            
            print(f"\n[{current_time.strftime('%H:%M:%S')}] Press Ctrl+C to exit...")
            time.sleep(2)
            clear_screen()
            print_header(bot_id)
            
        except KeyboardInterrupt:
            print("\nExiting botnet simulation...")
            break

if __name__ == "__main__":
    bot_id = 1
    if len(sys.argv) > 1:
        try:
            bot_id = int(sys.argv[1])
            if bot_id < 1 or bot_id > 3:
                bot_id = 1
        except ValueError:
            bot_id = 1
    
    simulate_botnet(bot_id) 