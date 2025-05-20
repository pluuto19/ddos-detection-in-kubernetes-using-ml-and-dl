#!/usr/bin/env python3
import argparse
import time
import random
import sys
import json
import os
from datetime import datetime, timedelta

class DataAggregatorSimulator:
    """
    Simulates a data aggregator service that collects metrics from K8s agents,
    processes them, and runs inference using ML models
    """
    def __init__(self):
        self.start_time = datetime.now() - timedelta(days=5, hours=7, minutes=23)
        self.connected_agents = 3
        self.database_connection = "OK"
        self.model_service = "OK"
        self.storage_used = 45.7
        self.storage_total = 500.0
        self.last_collection = datetime.now() - timedelta(seconds=30)
        self.metrics_collected = 384
        self.events_collected = 56
        
    def show_status(self):
        """Show the current status of the data aggregator"""
        uptime = datetime.now() - self.start_time
        uptime_days = uptime.days
        uptime_hours = uptime.seconds // 3600
        uptime_minutes = (uptime.seconds % 3600) // 60
        
        print("=== Data Aggregator Status ===")
        print(f"Status: Running")
        print(f"Uptime: {uptime_days} days, {uptime_hours} hours, {uptime_minutes} minutes")
        print(f"Connected agents: {self.connected_agents}")
        print(f"Database connection: {self.database_connection}")
        print(f"Model service: {self.model_service}")
        print("")
        print("=== Recent Data Collection ===")
        print(f"Last collection: {self.last_collection.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Metrics collected: {self.metrics_collected}")
        print(f"Events collected: {self.events_collected}")
        print(f"Storage usage: {self.storage_used} GB / {self.storage_total} GB")
        
    def process_data(self):
        """Simulate processing collected data"""
        print("[INFO] Starting data processing...")
        time.sleep(0.5)
        
        print("[INFO] Loading system metrics from agents...")
        time.sleep(1)
        
        print("[INFO] Processing network traffic data...")
        time.sleep(0.8)
        
        # Simulate anomaly detection
        print("[INFO] Detected anomaly in network traffic patterns")
        time.sleep(0.5)
        
        print("[INFO] Running inference on collected data...")
        time.sleep(1.5)
        
        # Simulate model prediction
        attack_type = "SYN Flood"
        confidence = round(random.uniform(95.0, 99.0), 1)
        print(f"[INFO] Model prediction: {attack_type} attack detected (confidence: {confidence}%)")
        time.sleep(0.5)
        
        print("[INFO] Storing results in database...")
        time.sleep(0.8)
        
        print("[INFO] Results stored successfully")
        time.sleep(0.3)
        
        print("[INFO] Sending alert to dashboard...")
        
    def run_inference(self, use_latest=True):
        """Simulate running inference with ML/DL models"""
        print("[INFO] Loading latest data for inference...")
        time.sleep(0.8)
        
        print("[INFO] Preparing features for model input...")
        time.sleep(1.2)
        
        # Simulate running different models
        print("[INFO] Running inference with RandomForest model...")
        time.sleep(0.7)
        
        print("[INFO] Running inference with LSTM model...")
        time.sleep(1.0)
        
        print("[INFO] Running inference with CNN model...")
        time.sleep(0.8)
        
        # Generate random confidence scores
        rf_confidence = round(random.uniform(95.0, 99.0), 1)
        lstm_confidence = round(random.uniform(95.0, 99.0), 1)
        cnn_confidence = round(random.uniform(95.0, 99.0), 1)
        
        # Calculate ensemble prediction
        ensemble_confidence = round((rf_confidence + lstm_confidence + cnn_confidence) / 3, 1)
        
        # Simulate model predictions
        attack_type = "SYN Flood"
        print("[INFO] Model predictions:")
        print(f"       - RandomForest: {attack_type} (confidence: {rf_confidence}%)")
        print(f"       - LSTM: {attack_type} (confidence: {lstm_confidence}%)")
        print(f"       - CNN: {attack_type} (confidence: {cnn_confidence}%)")
        time.sleep(0.5)
        
        print(f"[INFO] Ensemble prediction: {attack_type} (confidence: {ensemble_confidence}%)")
        time.sleep(0.3)
        
        print("[INFO] Storing prediction in database...")
        
    def collect_data(self):
        """Simulate collecting data from agents"""
        print("[INFO] Starting data collection from agents...")
        time.sleep(0.5)
        
        # Simulate collecting from each agent
        for i in range(1, 4):
            print(f"[INFO] Collecting metrics from k8s-worker-{i:02d}...")
            time.sleep(random.uniform(0.3, 0.7))
            
            # Generate random metrics count
            metrics_count = random.randint(100, 150)
            events_count = random.randint(10, 30)
            print(f"[INFO] Collected {metrics_count} metrics and {events_count} events from k8s-worker-{i:02d}")
            
        # Update collection stats
        self.last_collection = datetime.now()
        self.metrics_collected = random.randint(350, 450)
        self.events_collected = random.randint(40, 70)
        
        print(f"[INFO] Total metrics collected: {self.metrics_collected}")
        print(f"[INFO] Total events collected: {self.events_collected}")
        print("[INFO] Data collection completed successfully")
        
    def detect_attacks(self):
        """Simulate the attack detection pipeline"""
        # First collect data
        self.collect_data()
        time.sleep(1)
        
        # Then process it
        self.process_data()
        time.sleep(1)
        
        # Finally run inference
        self.run_inference()

def main():
    parser = argparse.ArgumentParser(description="Data Aggregator Simulator")
    parser.add_argument("--status", action="store_true", help="Show data aggregator status")
    parser.add_argument("--collect", action="store_true", help="Collect data from agents")
    parser.add_argument("--process", action="store_true", help="Process collected data")
    parser.add_argument("--inference", action="store_true", help="Run inference on collected data")
    parser.add_argument("--latest", action="store_true", help="Use latest data for inference")
    parser.add_argument("--detect", action="store_true", help="Run the full detection pipeline")
    
    args = parser.parse_args()
    
    simulator = DataAggregatorSimulator()
    
    if args.status:
        simulator.show_status()
    elif args.collect:
        simulator.collect_data()
    elif args.process:
        simulator.process_data()
    elif args.inference:
        simulator.run_inference(args.latest)
    elif args.detect:
        simulator.detect_attacks()
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 