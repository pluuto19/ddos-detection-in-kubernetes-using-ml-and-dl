#!/usr/bin/env python3
import os
import time
import random
import sys
from datetime import datetime

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(worker_id=1):
    """Print the terminal header"""
    hostname = f"k8s-worker-{worker_id:02d}"
    print("=" * 60)
    print(f"KUBERNETES WORKER NODE ({hostname})")
    print("=" * 60)
    print()

def simulate_k8s_worker(worker_id=1):
    """Simulate a Kubernetes worker node"""
    clear_screen()
    print_header(worker_id)
    
    # Track if we're under attack
    under_attack = False
    attack_type = None
    attack_start_time = None
    attack_duration = 0
    
    while True:
        try:
            current_time = datetime.now()
            
            # Randomly start an attack
            if not under_attack and random.random() < 0.1:  # 10% chance to start attack
                under_attack = True
                attack_types = ["SYN Flood", "HTTP Flood", "UDP Flood"]
                attack_type = random.choice(attack_types)
                attack_start_time = current_time
                attack_duration = random.randint(20, 40)  # Attack lasts 20-40 seconds
                print(f"\n[{current_time.strftime('%H:%M:%S')}] \033[91mALERT: Detecting high network traffic!\033[0m")
                print(f"[{current_time.strftime('%H:%M:%S')}] \033[91mPossible {attack_type} attack detected\033[0m")
            
            # End attack if duration has passed
            if under_attack and (current_time - attack_start_time).total_seconds() > attack_duration:
                under_attack = False
                print(f"\n[{current_time.strftime('%H:%M:%S')}] \033[92mNetwork traffic returning to normal\033[0m")
                print(f"[{current_time.strftime('%H:%M:%S')}] \033[92mSystem stabilizing\033[0m")
            
            # Show system info
            print(f"\n[{current_time.strftime('%H:%M:%S')}] Checking system status...")
            time.sleep(1)
            
            if under_attack:
                cpu_usage = random.uniform(70, 95)
                mem_usage = random.uniform(70, 90)
                network_in = random.uniform(800, 1500)  # MB/s
                network_out = random.uniform(100, 300)  # MB/s
            else:
                cpu_usage = random.uniform(10, 30)
                mem_usage = random.uniform(20, 50)
                network_in = random.uniform(5, 20)  # MB/s
                network_out = random.uniform(2, 10)  # MB/s
            
            print("\nSYSTEM INFO:")
            print(f"CPU Usage:    {cpu_usage:.1f}%")
            print(f"Memory Usage: {mem_usage:.1f}%")
            print(f"Network In:   {network_in:.1f} MB/s")
            print(f"Network Out:  {network_out:.1f} MB/s")
            print(f"Uptime:       45 days, 7 hours, 22 minutes")
            
            time.sleep(2)
            
            # Show network connections
            print(f"\n[{current_time.strftime('%H:%M:%S')}] Checking network connections...")
            time.sleep(1)
            
            print("\nNETWORK CONNECTIONS:")
            print("Proto Local Address           Foreign Address         State")
            print("tcp   0.0.0.0:22              0.0.0.0:*               LISTEN")
            print("tcp   0.0.0.0:10250           0.0.0.0:*               LISTEN")
            print("tcp   0.0.0.0:9100            0.0.0.0:*               LISTEN")
            
            if under_attack:
                if attack_type == "SYN Flood":
                    print("tcp   10.0.0.10:22            192.168.10.101:12345    SYN_RECV")
                    print("tcp   10.0.0.10:22            192.168.10.102:23456    SYN_RECV")
                    print("tcp   10.0.0.10:22            192.168.10.103:34567    SYN_RECV")
                    print("tcp   10.0.0.10:80            192.168.10.101:45678    SYN_RECV")
                    print("tcp   10.0.0.10:80            192.168.10.102:56789    SYN_RECV")
                    print("tcp   10.0.0.10:80            192.168.10.103:67890    SYN_RECV")
                    print("... (thousands more connections)")
                elif attack_type == "HTTP Flood":
                    print("tcp   10.0.0.10:80            192.168.10.101:12345    ESTABLISHED")
                    print("tcp   10.0.0.10:80            192.168.10.102:23456    ESTABLISHED")
                    print("tcp   10.0.0.10:80            192.168.10.103:34567    ESTABLISHED")
                    print("tcp   10.0.0.10:80            192.168.10.101:45678    ESTABLISHED")
                    print("tcp   10.0.0.10:80            192.168.10.102:56789    ESTABLISHED")
                    print("tcp   10.0.0.10:80            192.168.10.103:67890    ESTABLISHED")
                    print("... (thousands more connections)")
                elif attack_type == "UDP Flood":
                    print("udp   10.0.0.10:53            192.168.10.101:12345    ")
                    print("udp   10.0.0.10:53            192.168.10.102:23456    ")
                    print("udp   10.0.0.10:53            192.168.10.103:34567    ")
                    print("udp   10.0.0.10:53            192.168.10.101:45678    ")
                    print("udp   10.0.0.10:53            192.168.10.102:56789    ")
                    print("udp   10.0.0.10:53            192.168.10.103:67890    ")
                    print("... (thousands more connections)")
            
            time.sleep(2)
            
            # Show container status
            print(f"\n[{current_time.strftime('%H:%M:%S')}] Checking container status...")
            time.sleep(1)
            
            print("\nCONTAINER STATUS:")
            print("CONTAINER ID   IMAGE                    STATUS          NAMES")
            print("a7f8d9e6b5c4   k8s.io/pause:3.6         Up 45 days      k8s_POD_node-exporter")
            print("b6e7d8c9f0a1   prom/node-exporter:v1.3  Up 45 days      k8s_node-exporter")
            print("c5d6e7f8g9h0   falcosecurity/falco:0.32 Up 45 days      k8s_falco")
            print("d4e5f6g7h8i9   k8s.io/pause:3.6         Up 45 days      k8s_POD_falco")
            
            time.sleep(2)
            
            # Show logs
            print(f"\n[{current_time.strftime('%H:%M:%S')}] Checking system logs...")
            time.sleep(1)
            
            print("\nSYSTEM LOGS:")
            log_time = current_time.strftime("%Y-%m-%dT%H:%M:%SZ")
            print(f"{log_time} INFO  kubelet - Successfully registered node")
            print(f"{log_time} INFO  kubelet - Starting to sync pod")
            print(f"{log_time} INFO  node-exporter - Collecting metrics")
            
            if under_attack:
                if attack_type == "SYN Flood":
                    print(f"{log_time} WARN  kernel - TCP: request_sock_TCP: Possible SYN attack detected")
                    print(f"{log_time} WARN  kernel - TCP: Dropping {random.randint(1000, 5000)} packets due to overload")
                elif attack_type == "HTTP Flood":
                    print(f"{log_time} WARN  nginx - High number of HTTP connections")
                    print(f"{log_time} WARN  nginx - Worker connections exceeded, dropping requests")
                elif attack_type == "UDP Flood":
                    print(f"{log_time} WARN  kernel - UDP: Large number of UDP packets detected")
                    print(f"{log_time} WARN  kernel - UDP: Dropping {random.randint(1000, 5000)} packets due to overload")
            
            time.sleep(3)
            
            print(f"\n[{current_time.strftime('%H:%M:%S')}] Press Ctrl+C to exit...")
            time.sleep(2)
            
        except KeyboardInterrupt:
            print("\nExiting K8s worker simulation...")
            break

if __name__ == "__main__":
    worker_id = 1
    if len(sys.argv) > 1:
        try:
            worker_id = int(sys.argv[1])
            if worker_id < 1 or worker_id > 3:
                worker_id = 1
        except ValueError:
            worker_id = 1
    
    simulate_k8s_worker(worker_id) 