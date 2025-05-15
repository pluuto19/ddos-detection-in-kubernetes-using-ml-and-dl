#!/usr/bin/env python3
import socket
import json
import time
import threading
import requests
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from http.server import HTTPServer, BaseHTTPRequestHandler
import logging

INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "my-super-secret-auth-token"
INFLUXDB_ORG = "ddos_org"
INFLUXDB_BUCKET = "ddos_demo"

AGGREGATOR_HOST = '0.0.0.0'
AGGREGATOR_PORT = 12000
ANALYZER_HOST = 'localhost'
ANALYZER_PORT = 13000

node_data = {}
node_data_lock = threading.Lock()

class DataHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            node_id = self.headers.get('X-Node-ID', 'unknown-node')
            
            with node_data_lock:
                node_data[node_id] = data

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode())
            
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": "Invalid JSON"}).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode())

def send_to_analyzer():
    try:
        client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
        write_api = client.write_api(write_options=SYNCHRONOUS)
    except Exception as e:
        return
    
    while True:
        try:
            with node_data_lock:
                current_data = node_data.copy()
            
            if not current_data:
                time.sleep(3)
                continue
            
            aggregated_data = {
                "timestamp": time.time(),
                "nodes": current_data
            }
            
            response = requests.post(
                f"http://{ANALYZER_HOST}:{ANALYZER_PORT}/analyze",
                json=aggregated_data,
                timeout=5
            )
            
            if response.status_code == 200:
                analyzer_result = response.json()

                for node_id, node_metrics in current_data.items():
                    point = Point("kubernetes_metrics") \
                        .tag("node", node_id)
                    
                    if "resource_metrics" in node_metrics:
                        for metric_name, metric_value in node_metrics["resource_metrics"].items():
                            point = point.field(metric_name, metric_value)
                    
                    if "syscalls" in node_metrics:
                        total_syscalls = sum(node_metrics["syscalls"].values())
                        point = point.field("syscall_count", total_syscalls)
                        
                        for syscall_name, syscall_count in node_metrics["syscalls"].items():
                            point = point.field(f"syscall_{syscall_name}", syscall_count)
                    
                    if node_id in analyzer_result.get("nodes", {}):
                        node_analysis = analyzer_result["nodes"][node_id]
                        point = point \
                            .field("attack_detected", 1 if node_analysis.get("attack_detected", False) else 0) \
                            .field("attack_type", node_analysis.get("attack_type", "none")) \
                            .field("anomaly_score", node_analysis.get("anomaly_score", 0.0))
                    
                    write_api.write(bucket=INFLUXDB_BUCKET, record=point)
                
            else:
                print(f"Analyzer returned error: {response.status_code} - {response.text}")
        
        except requests.RequestException as e:
            print(f"Error communicating with analyzer: {e}")
        except Exception as e:
            print(f"Error in analyzer sender thread: {e}")
        
        time.sleep(3)

def main():
    server = HTTPServer((AGGREGATOR_HOST, AGGREGATOR_PORT), DataHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    analyzer_thread = threading.Thread(target=send_to_analyzer)
    analyzer_thread.daemon = True
    analyzer_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.shutdown()

if __name__ == "__main__":
    main() 