import socket
import json
import threading
import time
import random
import signal

PORT = 8545
ATTACK_TYPES = ["http", "tcp"]
DEFAULT_TARGETS = {
    "http": "http://load-test-server.default.svc.cluster.local",
    "tcp": "load-test-server.default.svc.cluster.local:5201"
}
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
        if not clients:
            print("No clients connected")
            return False
        
        client_count = len(clients)
        print(f"Sending command to {client_count} clients")
        
        clients_copy = clients.copy()
    
    success_count = 0
    for client_socket in clients_copy:
        try:
            if send_command(client_socket, command):
                success_count += 1
        except:
            pass
    
    print(f"Command sent to {success_count}/{client_count} clients")
    return success_count > 0

def start_attack(attack_type, target, duration):
    global current_attack, attack_end_time
    
    command = {
        "type": "attack",
        "attack_type": attack_type,
        "target": target,
        "duration": duration
    }
    
    success = send_to_all_clients(command)
    
    if success:
        current_attack = attack_type
        attack_end_time = time.time() + duration
        print(f"[{time.strftime('%H:%M:%S')}] Started {attack_type} attack for {duration} seconds")
    
    return success

def stop_attack():
    global current_attack, attack_end_time
    
    command = {"type": "stop"}
    success = send_to_all_clients(command)
    
    if success:
        current_attack = None
        attack_end_time = 0
        print(f"[{time.strftime('%H:%M:%S')}] Stopped all attacks")
    
    return success

def attack_manager():
    global current_attack, attack_end_time
    
    while True:
        with clients_lock:
            if not clients:
                print("Waiting for clients to connect...")
                time.sleep(5)
                continue
        
        current_time = time.time()
        
        if current_attack is None or current_time > attack_end_time:
            if current_attack is not None:
                print(f"[{time.strftime('%H:%M:%S')}] Previous attack completed")
                stop_attack()
                time.sleep(ATTACK_INTERVAL)
            
            attack_type = random.choice(ATTACK_TYPES)
            duration = random.randint(MIN_ATTACK_DURATION, MAX_ATTACK_DURATION)
            target = DEFAULT_TARGETS[attack_type]
            
            start_attack(attack_type, target, duration)
        
        time.sleep(5)

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind(('0.0.0.0', PORT))
        server_socket.listen(10)
        print(f"Attack controller started on port {PORT}")
        print(f"HTTP target: {DEFAULT_TARGETS['http']}")
        print(f"TCP target: {DEFAULT_TARGETS['tcp']}")
        
        accept_thread = threading.Thread(target=accept_clients, args=(server_socket,))
        accept_thread.daemon = True
        accept_thread.start()
        
        def signal_handler(sig, frame):
            print("\nShutting down controller...")
            try:
                stop_attack()
                server_socket.close()
            except:
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