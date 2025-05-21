#!/usr/bin/env python3
import time
import random
import json
from datetime import datetime
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# InfluxDB connection parameters
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "my-super-secret-auth-token"
INFLUXDB_ORG = "ddos_org"
INFLUXDB_BUCKET = "ddos_demo"

class DataAggregatorConnector:
    """
    Connects the simulation with InfluxDB to store metrics and attack data
    """
    def __init__(self):
        self.client = None
        self.write_api = None
        self.connected = False
        self.try_connect()
        
    def try_connect(self):
        """Try to connect to InfluxDB"""
        try:
            self.client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
            self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
            health = self.client.health()
            if health.status == "pass":
                self.connected = True
                print(f"✓ Connected to InfluxDB at {INFLUXDB_URL}")
                return True
            else:
                print(f"⚠️ InfluxDB is not healthy: {health.status}")
                return False
        except Exception as e:
            print(f"❌ Failed to connect to InfluxDB: {e}")
            return False
            
    def write_metrics(self, node_id, attack_type=None, attack_detected=False):
        """Write simulated metrics to InfluxDB"""
        if not self.connected:
            if not self.try_connect():
                print("Cannot write metrics: Not connected to InfluxDB")
                return False
        
        try:
            # Generate metrics based on attack status
            if attack_detected:
                metrics = self._generate_attack_metrics(attack_type)
            else:
                metrics = self._generate_normal_metrics()
                
            point = Point("kubernetes_metrics") \
                .tag("node", node_id) \
                .tag("attack_type", metrics["attack_type"]) \
                .field("cpu_usage", metrics["cpu_usage"]) \
                .field("memory_usage", metrics["memory_usage"]) \
                .field("network_in", metrics["network_in"]) \
                .field("network_out", metrics["network_out"]) \
                .field("syscall_count", metrics["syscall_count"]) \
                .field("attack_detected", metrics["attack_detected"]) \
                .field("anomaly_score", metrics["anomaly_score"]) \
                .field("attack_type_field", metrics["attack_type"])
                
            self.write_api.write(bucket=INFLUXDB_BUCKET, record=point)
            
            # Print status
            current_time = datetime.now().strftime("%H:%M:%S")
            attack_status = "🔴 ATTACK" if metrics["attack_detected"] == 1 else "🟢 NORMAL"
            print(f"[{current_time}] ✓ {attack_status} | Node: {node_id} | CPU: {metrics['cpu_usage']:.1f}% | Score: {metrics['anomaly_score']:.2f}")
            
            return True
        except Exception as e:
            print(f"Error writing to InfluxDB: {e}")
            self.connected = False
            return False
            
    def _generate_normal_metrics(self):
        """Generate metrics for normal system operation"""
        return {
            "cpu_usage": random.uniform(10, 30),  # 10-30%
            "memory_usage": random.uniform(1000, 3000),  # 1000-3000 MB
            "network_in": random.uniform(500000, 2000000),  # 500KB-2MB/s
            "network_out": random.uniform(200000, 1000000),  # 200KB-1MB/s
            "syscall_count": random.randint(100, 500),
            "attack_detected": 0,
            "attack_type": "none",
            "anomaly_score": random.uniform(0, 0.2)  # 0-0.2 (low)
        }
        
    def _generate_attack_metrics(self, attack_type="SYN Flood"):
        """Generate metrics for system under attack"""
        # Base metrics with higher values indicating attack
        metrics = {
            "cpu_usage": random.uniform(70, 95),  # 70-95%
            "memory_usage": random.uniform(5000, 8000),  # 5000-8000 MB
            "syscall_count": random.randint(2000, 10000),
            "attack_detected": 1,
            "attack_type": attack_type.lower().replace(" ", "_"),
            "anomaly_score": random.uniform(0.7, 0.98)  # 0.7-0.98 (high)
        }
        
        # Customize metrics based on attack type
        if "http" in attack_type.lower():
            metrics["network_in"] = random.uniform(10000000, 20000000)  # 10-20MB/s
            metrics["network_out"] = random.uniform(5000000, 10000000)  # 5-10MB/s
        elif "syn" in attack_type.lower() or "tcp" in attack_type.lower():
            metrics["network_in"] = random.uniform(15000000, 25000000)  # 15-25MB/s
            metrics["network_out"] = random.uniform(1000000, 3000000)  # 1-3MB/s
        else:  # udp
            metrics["network_in"] = random.uniform(20000000, 30000000)  # 20-30MB/s
            metrics["network_out"] = random.uniform(500000, 1500000)  # 0.5-1.5MB/s
        
        return metrics
        
    def simulate_attack_detection(self, attack_type, duration=30):
        """Simulate an attack and its detection"""
        print(f"Simulating {attack_type} attack detection for {duration} seconds...")
        
        nodes = [f"k8s-worker-{i:02d}" for i in range(1, 4)]
        
        # Write pre-attack metrics
        for node in nodes:
            self.write_metrics(node)
            time.sleep(0.5)
            
        # Write attack metrics
        start_time = time.time()
        while time.time() - start_time < duration:
            for node in nodes:
                self.write_metrics(node, attack_type, True)
                time.sleep(1)
                
        # Write post-attack metrics
        for node in nodes:
            self.write_metrics(node)
            time.sleep(0.5)
            
        print(f"Attack simulation completed.")
        
    def close(self):
        """Close the InfluxDB connection"""
        if self.client:
            self.client.close()
            print("InfluxDB connection closed")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Data Aggregator Connector")
    parser.add_argument("--attack", choices=["syn_flood", "http_flood", "udp_flood"], 
                        help="Simulate an attack of the specified type")
    parser.add_argument("--duration", type=int, default=30, 
                        help="Duration of the attack simulation in seconds")
    parser.add_argument("--metrics", action="store_true", 
                        help="Write a single set of metrics to InfluxDB")
    
    args = parser.parse_args()
    
    connector = DataAggregatorConnector()
    
    try:
        if args.attack:
            attack_type = args.attack.replace("_", " ").title()
            connector.simulate_attack_detection(attack_type, args.duration)
        elif args.metrics:
            for i in range(1, 4):
                connector.write_metrics(f"k8s-worker-{i:02d}")
        else:
            print("No action specified. Use --attack or --metrics")
    finally:
        connector.close() 