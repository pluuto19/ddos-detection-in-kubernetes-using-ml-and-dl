import socket
import json
import threading
import time
import random
import sys
import signal

PORT = 8545
ATTACK_TYPES = ["http", "tcp"]
DEFAULT_TARGETS = {
    "http": "http://load-test-server.default.svc.cluster.local",
    "tcp": "load-test-server.default.svc.cluster.local:5201"
}
MIN_ATTACK_DURATION = 240
MAX_ATTACK_DURATION = 480
ATTACK_INTERVAL = 5

clients = []
clients_lock = threading.Lock()
current_attack = None
attack_end_time = 0

def send_command(client_socket, command):
    try:
        client_socket.sendall(json.dumps(command).encode('utf-8'))
        return True
    except Exception as e:
        print(f"Error sending command: {e}")
        return False

def handle_client(client_socket, client_address):
    client_id = f"{client_address[0]}:{client_address[1]}"
    print(f"New client connected: {client_id}")
    
    if not send_command(client_socket, {"type": "ping"}):
        print(f"Failed to send initial ping to {client_id}, disconnecting")
        remove_client(client_socket)
        return
    
    while True:
        try:
            data = client_socket.recv(4096)
            if not data:
                print(f"Client disconnected: {client_id}")
                break
            
            try:
                message = json.loads(data.decode('utf-8'))
                message_type = message.get("type")
                
                if message_type == "status":
                    status = message.get("status")
                    attack_type = message.get("attack_type", "unknown")
                    container_id = message.get("container_id", "unknown")
                    
                    if status == "attack_started":
                        print(f"Client {client_id} started {attack_type} attack with container {container_id[:12]}")
                    elif status == "stopped":
                        print(f"Client {client_id} stopped attack")
                
                elif message_type == "error":
                    print(f"Error from client {client_id}: {message.get('message', 'Unknown error')}")
                
            except json.JSONDecodeError:
                print(f"Invalid JSON from client {client_id}: {data.decode('utf-8')}")
        
        except Exception as e:
            print(f"Error handling client {client_id}: {e}")
            break
    
    remove_client(client_socket)

def remove_client(client_socket):
    with clients_lock:
        if client_socket in clients:
            clients.remove(client_socket)
    
    try:
        client_socket.close()
    except:
        pass

def accept_clients(server_socket):
    while True:
        try:
            client_socket, client_address = server_socket.accept()
            
            with clients_lock:
                clients.append(client_socket)
            
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address)
            )
            client_thread.daemon = True
            client_thread.start()
            
        except Exception as e:
            print(f"Error accepting client: {e}")
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
            
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        print("Auto-attack mode enabled. Press Ctrl+C to exit.")
        
        attack_manager()
        
    except KeyboardInterrupt:
        print("\nShutting down controller...")
    except Exception as e:
        print(f"Server error: {e}")
    
    finally:
        try:
            stop_attack()
            server_socket.close()
        except:
            pass

if __name__ == "__main__":
    main()