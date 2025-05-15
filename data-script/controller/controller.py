import socket
import json
import threading
import time
import random
import signal
import sys

REQUIRED_CLIENTS = 3

HTTP_TARGET = "http://service.default:8080"
TCP_TARGET_HOST = "service.default"
TCP_TARGET_PORT = 5001

HTTP_THREADS = [2, 4, 8]
HTTP_CONNECTIONS = [50, 100, 200]
TCP_PARALLEL = [2, 4, 8, 16]
TCP_BANDWIDTH = ["0"]

MIN_ATTACK_DURATION = 240
MAX_ATTACK_DURATION = 480

PORT = 8545

clients = []
clients_lock = threading.Lock()
running = True

def accept_clients(server_socket):
    while running:
        try:
            client_socket, client_address = server_socket.accept()
            with clients_lock:
                clients.append(client_socket)
        except Exception:
            time.sleep(1)

def send_to_all_clients(command):
    with clients_lock:
        for client in clients:
            try:
                client.sendall(json.dumps(command).encode('utf-8'))
            except Exception:
                pass

def wait_for_clients():
    while running:
        with clients_lock:
            if len(clients) >= REQUIRED_CLIENTS:
                return
        time.sleep(2)

def main_loop():
    while running:
        # Randomly choose attack type and duration
        attack_type = random.choice(["http", "tcp"])
        duration = random.randint(MIN_ATTACK_DURATION, MAX_ATTACK_DURATION)

        if attack_type == "http":
            threads = random.choice(HTTP_THREADS)
            connections = random.choice(HTTP_CONNECTIONS)
            command = {
                "type": "attack",
                "attack_type": "http",
                "target": HTTP_TARGET,
                "duration": duration,
                "threads": threads,
                "connections": connections
            }
        else:
            parallel = random.choice(TCP_PARALLEL)
            bandwidth = random.choice(TCP_BANDWIDTH)
            command = {
                "type": "attack",
                "attack_type": "tcp",
                "host": TCP_TARGET_HOST,
                "port": TCP_TARGET_PORT,
                "duration": duration,
                "parallel": parallel,
                "bandwidth": bandwidth
            }

        send_to_all_clients(command)
        time.sleep(duration)

        # Stop attack
        send_to_all_clients({"type": "stop"})
        time.sleep(5)  # Short pause before next attack

def cleanup(*_):
    global running
    running = False
    with clients_lock:
        for client in clients:
            try:
                client.close()
            except Exception:
                pass
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', PORT))
    server_socket.listen(10)

    threading.Thread(target=accept_clients, args=(server_socket,), daemon=True).start()

    wait_for_clients()
    main_loop()