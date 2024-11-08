import socket
import json
import csv
import random
import time
import threading
from datetime import datetime

PORT = 7745
MODES = ["normal_traffic", "high_traffic", "udp_flood", "tcp_flood", "http_flood", "icmp_flood"]
CSV_FILE = "collected_data.csv"
EXP_CONNS = 2

HEADERS = [
    "timestamp", "mode", "hostname", "output", "evt_time", "syscall_type", "priority", "rule", "source", "tags",
    "node_cpu_seconds_total", "node_filesystem_avail_bytes", "node_filesystem_size_bytes", 
    "node_disk_read_bytes_total", "node_disk_written_bytes_total", "node_network_receive_bytes_total", 
    "node_network_receive_drop_total", "node_network_receive_errs_total", "node_network_transmit_packets_total",
    "node_vmstat_pgmajfault", "node_memory_MemAvailable_bytes", "node_memory_MemTotal_bytes", 
    "node_forks_total", "node_intr_total", "node_load1", "node_load5", "node_load15", 
    "node_sockstat_TCP_alloc", "node_sockstat_TCP_inuse", "node_sockstat_TCP_mem", 
    "node_sockstat_TCP_mem_bytes", "node_sockstat_UDP_inuse", "node_sockstat_UDP_mem", 
    "node_sockstat_sockets_used", "node_netstat_Tcp_CurrEstab", "node_filefd_allocated"
]

current_mode = MODES[0]
clients = []
mode_lock = threading.Lock()
client_lock = threading.Lock()

def save_to_csv(data):
    with open(CSV_FILE, mode='a', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=HEADERS)
        writer.writerow(data)

def handle_client_connection(client_socket):
    global current_mode
    with client_lock:
        clients.append(client_socket)
    while True:
        try:
            data = client_socket.recv(4096).decode()
            if data:
                json_data = json.loads(data)
                entry = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "mode": current_mode,
                    "hostname": json_data.get("Hostname"),
                    "output": json_data.get("Output"),
                    "evt_time": json_data["OutputFields"].get("evt.time"),
                    "syscall_type": json_data["OutputFields"].get("syscall.type"),
                    "priority": json_data.get("Priority"),
                    "rule": json_data.get("Rule"),
                    "source": json_data.get("Source"),
                    "tags": ",".join(json_data.get("Tags", [])),
                    **{metric: json_data.get(metric, None) for metric in HEADERS[10:]}
                }
                save_to_csv(entry)
        
        except (json.JSONDecodeError, KeyError):
            continue

def notify_clients(new_mode):
    with client_lock:
        for client in clients:
            try:
                client.sendall(new_mode.encode())
            except BrokenPipeError:
                clients.remove(client)

def mode_switcher():
    global current_mode
    while True:
        with mode_lock:
            new_mode = random.choice(MODES)
            current_mode = new_mode
            notify_clients(new_mode)
        time.sleep(random.randint(5, 15))

def start_controller():
    conn_count = 0
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("", PORT))
    server_socket.listen(5)

    while True:
        client_socket, client_address = server_socket.accept()
        client_socket.sendall(current_mode.encode())
        threading.Thread(target=handle_client_connection, args=(client_socket,), daemon=True).start()
        conn_count += 1
        if conn_count == EXP_CONNS:
            threading.Thread(target=mode_switcher, daemon=True).start()

if __name__ == "__main__":
    with open(CSV_FILE, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=HEADERS)
        writer.writeheader()

    start_controller()
