#!/usr/bin/env python3
import argparse
import time
import random
import sys
from datetime import datetime

class AttackSimulator:
    """
    Simulates different types of DoS/DDoS attacks
    """
    def __init__(self, attack_type, target, duration, threads=8, rate=10000):
        self.attack_type = attack_type
        self.target = target
        self.duration = duration
        self.threads = threads
        self.rate = rate
        
    def print_progress(self, progress):
        """Print a progress bar"""
        bar_length = 20
        filled_length = int(bar_length * progress)
        bar = '▓' * filled_length + ' ' * (bar_length - filled_length)
        sys.stdout.write(f"\r[*] Progress: {bar} {int(progress * 100)}%")
        sys.stdout.flush()
        
    def syn_flood(self):
        """Simulate a SYN flood attack"""
        print(f"[*] Preparing SYN Flood attack against {self.target}")
        print(f"[*] Attack parameters: threads={self.threads}, packets_per_second={self.rate}")
        print(f"[*] Starting attack for {self.duration} seconds...")
        print(f"[*] Sending SYN packets...")
        
        start_time = time.time()
        total_packets = self.duration * self.rate
        packets_sent = 0
        
        while time.time() - start_time < self.duration:
            # Simulate sending packets
            elapsed = time.time() - start_time
            progress = min(elapsed / self.duration, 1.0)
            packets_sent = int(progress * total_packets)
            
            self.print_progress(progress)
            time.sleep(0.1)
            
        print(f"\n[*] Attack completed. Sent {packets_sent} packets.")
        
    def http_flood(self):
        """Simulate an HTTP flood attack"""
        print(f"[*] Preparing HTTP Flood attack against {self.target}")
        print(f"[*] Attack parameters: threads={self.threads}, requests_per_second={self.rate // 2}")
        print(f"[*] Starting attack for {self.duration} seconds...")
        print(f"[*] Sending HTTP requests...")
        
        start_time = time.time()
        total_requests = self.duration * (self.rate // 2)
        requests_sent = 0
        
        while time.time() - start_time < self.duration:
            # Simulate sending requests
            elapsed = time.time() - start_time
            progress = min(elapsed / self.duration, 1.0)
            requests_sent = int(progress * total_requests)
            
            self.print_progress(progress)
            time.sleep(0.1)
            
        print(f"\n[*] Attack completed. Sent {requests_sent} requests.")
        
    def udp_flood(self):
        """Simulate a UDP flood attack"""
        print(f"[*] Preparing UDP Flood attack against {self.target}")
        print(f"[*] Attack parameters: threads={self.threads}, packets_per_second={self.rate * 1.5}")
        print(f"[*] Starting attack for {self.duration} seconds...")
        print(f"[*] Sending UDP packets...")
        
        start_time = time.time()
        total_packets = self.duration * int(self.rate * 1.5)
        packets_sent = 0
        
        while time.time() - start_time < self.duration:
            # Simulate sending packets
            elapsed = time.time() - start_time
            progress = min(elapsed / self.duration, 1.0)
            packets_sent = int(progress * total_packets)
            
            self.print_progress(progress)
            time.sleep(0.1)
            
        print(f"\n[*] Attack completed. Sent {packets_sent} packets.")
        
    def run_attack(self):
        """Run the selected attack type"""
        if self.attack_type == "syn_flood":
            self.syn_flood()
        elif self.attack_type == "http_flood":
            self.http_flood()
        elif self.attack_type == "udp_flood":
            self.udp_flood()
        else:
            print(f"[!] Unknown attack type: {self.attack_type}")
            print(f"[!] Supported types: syn_flood, http_flood, udp_flood")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="DoS/DDoS Attack Simulator")
    parser.add_argument("--type", required=True, help="Attack type (syn_flood, http_flood, udp_flood)")
    parser.add_argument("--target", required=True, help="Target IP address or hostname")
    parser.add_argument("--duration", type=int, default=30, help="Attack duration in seconds")
    parser.add_argument("--threads", type=int, default=8, help="Number of threads to use")
    parser.add_argument("--rate", type=int, default=10000, help="Packets/requests per second")
    
    args = parser.parse_args()
    
    simulator = AttackSimulator(
        attack_type=args.type,
        target=args.target,
        duration=args.duration,
        threads=args.threads,
        rate=args.rate
    )
    
    simulator.run_attack()

if __name__ == "__main__":
    main() 