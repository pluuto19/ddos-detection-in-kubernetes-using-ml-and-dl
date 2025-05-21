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
    print("DATA AGGREGATOR SERVER (data-aggregator)")
    print("=" * 60)
    print()

def simulate_data_aggregator():
    """Simulate a data aggregator server"""
    clear_screen()
    print_header()
    
    # Server state
    connected_nodes = ["k8s-worker-01", "k8s-worker-02", "k8s-worker-03"]
    metrics_collected = 0
    events_collected = 0
    attack_detected = False
    attack_type = None
    attack_start_time = None
    attack_duration = 0
    model_confidence = 0.0
    
    print("[*] Data aggregator service started")
    print("[*] Connected to InfluxDB")
    print("[*] Machine learning models loaded")
    print("[*] Waiting for metrics from nodes...")
    time.sleep(1)
    
    while True:
        try:
            current_time = datetime.now()
            
            # Randomly detect an attack
            if not attack_detected and random.random() < 0.05:  # 5% chance to detect attack
                attack_detected = True
                attack_types = ["SYN Flood", "HTTP Flood", "UDP Flood"]
                attack_type = random.choice(attack_types)
                attack_start_time = current_time
                attack_duration = random.randint(20, 40)
                model_confidence = random.uniform(0.92, 0.99)
                
                print(f"\n[{current_time.strftime('%H:%M:%S')}] \033[91mALERT: Anomaly detected in network traffic!\033[0m")
                print(f"[{current_time.strftime('%H:%M:%S')}] \033[91mPossible {attack_type} attack detected\033[0m")
                print(f"[{current_time.strftime('%H:%M:%S')}] \033[91mModel confidence: {model_confidence:.2f}\033[0m")
                print(f"[{current_time.strftime('%H:%M:%S')}] \033[91mStoring detection event in InfluxDB\033[0m")
            
            # End attack if duration has passed
            if attack_detected and (current_time - attack_start_time).total_seconds() > attack_duration:
                attack_detected = False
                print(f"\n[{current_time.strftime('%H:%M:%S')}] \033[92mNetwork traffic returning to normal\033[0m")
                print(f"[{current_time.strftime('%H:%M:%S')}] \033[92mNo anomalies detected in recent data\033[0m")
                print(f"[{current_time.strftime('%H:%M:%S')}] \033[92mUpdating InfluxDB with normal status\033[0m")
                attack_type = None
            
            # Collect metrics
            new_metrics = random.randint(10, 30)
            new_events = random.randint(1, 5)
            metrics_collected += new_metrics
            events_collected += new_events
            
            print(f"\n[{current_time.strftime('%H:%M:%S')}] Collecting metrics from nodes...")
            
            for node in connected_nodes:
                time.sleep(0.5)
                node_metrics = random.randint(3, 10)
                node_events = random.randint(0, 2)
                print(f"[{current_time.strftime('%H:%M:%S')}] Received {node_metrics} metrics and {node_events} events from {node}")
            
            print(f"[{current_time.strftime('%H:%M:%S')}] Total metrics collected: {metrics_collected}")
            print(f"[{current_time.strftime('%H:%M:%S')}] Total events collected: {events_collected}")
            
            # Process data
            print(f"\n[{current_time.strftime('%H:%M:%S')}] Processing collected data...")
            time.sleep(1)
            
            print(f"[{current_time.strftime('%H:%M:%S')}] Running feature extraction...")
            time.sleep(0.5)
            
            print(f"[{current_time.strftime('%H:%M:%S')}] Running anomaly detection...")
            time.sleep(0.5)
            
            # Run model inference
            print(f"\n[{current_time.strftime('%H:%M:%S')}] Running model inference...")
            time.sleep(1)
            
            # Show model results
            rf_confidence = random.uniform(0.5, 0.99)
            lstm_confidence = random.uniform(0.5, 0.99)
            cnn_confidence = random.uniform(0.5, 0.99)
            
            if attack_detected:
                rf_confidence = random.uniform(0.85, 0.99)
                lstm_confidence = random.uniform(0.85, 0.99)
                cnn_confidence = random.uniform(0.85, 0.99)
                
                print(f"[{current_time.strftime('%H:%M:%S')}] RandomForest: {attack_type} detected (confidence: {rf_confidence:.2f})")
                print(f"[{current_time.strftime('%H:%M:%S')}] LSTM: {attack_type} detected (confidence: {lstm_confidence:.2f})")
                print(f"[{current_time.strftime('%H:%M:%S')}] CNN: {attack_type} detected (confidence: {cnn_confidence:.2f})")
                print(f"[{current_time.strftime('%H:%M:%S')}] Ensemble: {attack_type} detected (confidence: {model_confidence:.2f})")
            else:
                print(f"[{current_time.strftime('%H:%M:%S')}] RandomForest: No attack detected (confidence: {rf_confidence:.2f})")
                print(f"[{current_time.strftime('%H:%M:%S')}] LSTM: No attack detected (confidence: {lstm_confidence:.2f})")
                print(f"[{current_time.strftime('%H:%M:%S')}] CNN: No attack detected (confidence: {cnn_confidence:.2f})")
                print(f"[{current_time.strftime('%H:%M:%S')}] Ensemble: No attack detected (confidence: {(rf_confidence + lstm_confidence + cnn_confidence) / 3:.2f})")
            
            # Store results
            print(f"\n[{current_time.strftime('%H:%M:%S')}] Storing results in InfluxDB...")
            time.sleep(0.5)
            
            print(f"[{current_time.strftime('%H:%M:%S')}] Results stored successfully")
            
            # System stats
            print(f"\n[{current_time.strftime('%H:%M:%S')}] System Status:")
            print(f"CPU Usage:    {random.uniform(20, 40):.1f}%")
            print(f"Memory Usage: {random.uniform(30, 60):.1f}%")
            print(f"Storage:      {random.uniform(40, 60):.1f}% used")
            print(f"Connected nodes: {len(connected_nodes)}")
            
            print(f"\n[{current_time.strftime('%H:%M:%S')}] Press Ctrl+C to exit...")
            time.sleep(5)
            clear_screen()
            print_header()
            
        except KeyboardInterrupt:
            print("\nExiting data aggregator simulation...")
            break

if __name__ == "__main__":
    simulate_data_aggregator() 