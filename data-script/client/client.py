import socket
import subprocess
import os
import signal
import time
from pathlib import Path

PORT_CMD = 7745
BINARY_PATH = Path("./tools")
current_process = None
current_mode = None
sock = None
mode_binaries = {
    "normal_traffic": ("normal_traffic_binary", ["--mode", "normal"]),
    "high_traffic": ("high_traffic_binary", ["--mode", "high"]),
    "udp_flood": ("flood_binary", ["--type", "udp"]),
    "tcp_flood": ("flood_binary", ["--type", "tcp"]),
    "http_flood": ("flood_binary", ["--type", "http"]),
    "icmp_flood": ("flood_binary", ["--type", "icmp"])
}

def connect_to_controller():
    global sock
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("localhost", PORT_CMD))
            print(f"Connected to controller at localhost:{PORT_CMD}")
            return
        except ConnectionRefusedError:
            print("Retrying in 5 seconds")
            time.sleep(5)

def launch_process(mode):
    global current_process
    binary_name, args = mode_binaries[mode]
    binary_path = BINARY_PATH / binary_name

    if not binary_path.exists():
        print(f"Binary not found: {binary_path}")
        return False

    try:
        process = subprocess.Popen(
            [str(binary_path)] + args,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        current_process = process
        print(f"Launched process for mode {mode} with PID {process.pid}")
        return True
    except Exception as e:
        print(f"Failed to launch process: {e}")
        return False

def kill_current_process():
    global current_process
    if current_process:
        try:
            os.kill(current_process.pid, signal.SIGKILL)
            current_process.wait(timeout=5)
        except ProcessLookupError:
            pass
        print(f"Killed process with PID {current_process.pid}")
        current_process = None

def handle_mode_change(new_mode):
    global current_mode
    if new_mode != current_mode:
        print(f"Mode change detected: {new_mode}")
        kill_current_process()
        if launch_process(new_mode):
            current_mode = new_mode

def run():
    global sock
    while True:
        try:
            if not sock:
                connect_to_controller()

            mode = sock.recv(1024).decode().strip()
            if not mode:
                print("Lost connection to controller")
                sock.close()
                sock = None
                continue

            handle_mode_change(mode)

        except socket.error as e:
            print(f"Socket error: {e}")
            if sock:
                sock.close()
                sock = None
            time.sleep(5)
        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(5)

def cleanup():
    kill_current_process()
    if sock:
        sock.close()

if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\nShutting down client...")
    finally:
        cleanup()