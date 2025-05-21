#!/usr/bin/env python3
import os
import sys
import subprocess
import time

def run_dashboard_generator():
    """Run the dashboard data generator"""
    dashboard_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dashboard")
    generator_path = os.path.join(dashboard_dir, "data_generator.py")
    
    if not os.path.exists(generator_path):
        print(f"Error: Dashboard data generator not found at {generator_path}")
        return False
    
    print("=" * 60)
    print("STARTING DASHBOARD DATA GENERATOR")
    print("=" * 60)
    print()
    print("This will generate data for the Grafana dashboard.")
    print("The data will be stored in InfluxDB.")
    print()
    print("Make sure InfluxDB is running (see docker-compose.yml in the dashboard directory).")
    print()
    print("Press Ctrl+C to stop the data generator.")
    print()
    
    try:
        # Run the data generator
        process = subprocess.Popen([sys.executable, generator_path])
        
        # Wait for the process to finish or for the user to interrupt
        while process.poll() is None:
            time.sleep(1)
            
        return True
    except KeyboardInterrupt:
        print("\nStopping dashboard data generator...")
        if process and process.poll() is None:
            process.terminate()
        return True
    except Exception as e:
        print(f"Error running dashboard data generator: {e}")
        return False

if __name__ == "__main__":
    run_dashboard_generator() 