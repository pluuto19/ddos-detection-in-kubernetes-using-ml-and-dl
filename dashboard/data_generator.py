#!/usr/bin/env python3
import random
import time
import datetime
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# InfluxDB connection parameters
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "my-super-secret-auth-token"
INFLUXDB_ORG = "ddos_org"
INFLUXDB_BUCKET = "ddos_demo"

# Connect to InfluxDB
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Attack types
ATTACK_TYPES = ["none", "http", "tcp", "udp"]

# Current system state
current_state = {
    "under_attack": False,
    "attack_type": "none",
    "phase_end_time": time.time() + random.randint(240, 480)  # 4-8 minutes
}

def generate_normal_metrics():
    """Generate metrics for normal system operation."""
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

def generate_attack_metrics():
    """Generate metrics for system under attack."""
    attack_type = random.choice(["http", "tcp", "udp"])
    
    # Base metrics with higher values indicating attack
    metrics = {
        "cpu_usage": random.uniform(70, 95),  # 70-95%
        "memory_usage": random.uniform(5000, 8000),  # 5000-8000 MB
        "syscall_count": random.randint(2000, 10000),
        "attack_detected": 1,
        "attack_type": attack_type,
        "anomaly_score": random.uniform(0.7, 0.98)  # 0.7-0.98 (high)
    }
    
    # Customize metrics based on attack type
    if attack_type == "http":
        metrics["network_in"] = random.uniform(10000000, 20000000)  # 10-20MB/s
        metrics["network_out"] = random.uniform(5000000, 10000000)  # 5-10MB/s
    elif attack_type == "tcp":
        metrics["network_in"] = random.uniform(15000000, 25000000)  # 15-25MB/s
        metrics["network_out"] = random.uniform(1000000, 3000000)  # 1-3MB/s
    else:  # udp
        metrics["network_in"] = random.uniform(20000000, 30000000)  # 20-30MB/s
        metrics["network_out"] = random.uniform(500000, 1500000)  # 0.5-1.5MB/s
    
    return metrics

def switch_phase_if_needed():
    """Switch between normal and attack phases based on time."""
    current_time = time.time()
    
    if current_time > current_state["phase_end_time"]:
        # Switch phase
        current_state["under_attack"] = not current_state["under_attack"]
        
        # Set new phase duration (4-8 minutes)
        current_state["phase_end_time"] = current_time + random.randint(240, 480)
        
        if current_state["under_attack"]:
            current_state["attack_type"] = random.choice(["http", "tcp", "udp"])
            print(f"⚠️ Attack phase started: {current_state['attack_type']} attack")
        else:
            current_state["attack_type"] = "none"
            print("✓ Normal phase started")

def write_metrics_to_influxdb(metrics):
    """Write metrics to InfluxDB."""
    point = Point("kubernetes_metrics") \
        .tag("node", "node1") \
        .tag("pod", "pod-simulator") \
        .tag("attack_type", metrics["attack_type"]) \
        .field("cpu_usage", metrics["cpu_usage"]) \
        .field("memory_usage", metrics["memory_usage"]) \
        .field("network_in", metrics["network_in"]) \
        .field("network_out", metrics["network_out"]) \
        .field("syscall_count", metrics["syscall_count"]) \
        .field("attack_detected", metrics["attack_detected"]) \
        .field("anomaly_score", metrics["anomaly_score"]) \
        .field("attack_type_field", metrics["attack_type"])
    
    try:
        write_api.write(bucket=INFLUXDB_BUCKET, record=point)
        return True
    except Exception as e:
        print(f"Error writing to InfluxDB: {e}")
        return False

def main():
    """Main function to generate and send metrics."""
    print("🚀 Starting DDoS Detection Simulator")
    print("Metrics will be sent to InfluxDB every 3 seconds")
    print(f"InfluxDB URL: {INFLUXDB_URL}")
    print(f"Organization: {INFLUXDB_ORG}")
    print(f"Bucket: {INFLUXDB_BUCKET}")
    print("Press Ctrl+C to stop")
    
    # Test InfluxDB connection
    try:
        health = client.health()
        if health.status == "pass":
            print("✓ Successfully connected to InfluxDB")
        else:
            print(f"⚠️ InfluxDB is not healthy: {health.status}")
    except Exception as e:
        print(f"❌ Failed to connect to InfluxDB: {e}")
    
    try:
        while True:
            switch_phase_if_needed()
            
            if current_state["under_attack"]:
                metrics = generate_attack_metrics()
                metrics["attack_type"] = current_state["attack_type"]
            else:
                metrics = generate_normal_metrics()
            
            success = write_metrics_to_influxdb(metrics)
            
            # Print current metric summary to console
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            attack_status = "🔴 ATTACK" if metrics["attack_detected"] == 1 else "🟢 NORMAL"
            status_icon = "✓" if success else "❌"
            print(f"[{current_time}] {status_icon} {attack_status} | CPU: {metrics['cpu_usage']:.1f}% | Mem: {metrics['memory_usage']:.0f}MB | Score: {metrics['anomaly_score']:.2f}")
            
            time.sleep(3)  # Send metrics every 3 seconds
            
    except KeyboardInterrupt:
        print("\n⛔ Stopping DDoS Detection Simulator")
        client.close()

if __name__ == "__main__":
    main() 