import socket
import time
import random
import argparse
import threading
from concurrent.futures import ThreadPoolExecutor
import math
import signal
import sys
from threading import Event
import logging
from contextlib import contextmanager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TrafficGenerator:
    def __init__(self, mode="normal"):
        self.mode = mode
        self.shutdown_event = Event()
        self.current_connections = 0
        self.lock = threading.Lock()
        self.connection_attempts = 0
        self.max_retries = 3
        self.socket_timeout = 5
        
        if mode == "normal":
            self.max_concurrent = 50
            self.ramp_time = 30
            self.sustain_time = 60
            self.cooldown_time = 30
            self.max_total_connections = 1000
        else:
            self.max_concurrent = 200
            self.ramp_time = 45
            self.sustain_time = 90
            self.cooldown_time = 45
            self.max_total_connections = 5000
        
        self.target_ports = [80]
        
        for sig in [signal.SIGINT, signal.SIGTERM]:
            signal.signal(sig, self.handle_shutdown)
            
        self.active_sockets = set()
        self.pool_lock = threading.Lock()

    @contextmanager
    def managed_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.socket_timeout)
        try:
            with self.pool_lock:
                self.active_sockets.add(sock)
            yield sock
        finally:
            with self.pool_lock:
                self.active_sockets.discard(sock)
            try:
                sock.shutdown(socket.SHUT_RDWR)
            except:
                pass
            try:
                sock.close()
            except:
                pass

    def handle_shutdown(self, signum, frame):
        logger.info("Initiating graceful shutdown...")
        self.shutdown_event.set()
        
        with self.pool_lock:
            for sock in self.active_sockets:
                try:
                    sock.shutdown(socket.SHUT_RDWR)
                    sock.close()
                except:
                    pass
            self.active_sockets.clear()
        
        logger.info("Shutdown complete")
        sys.exit(0)

    def calculate_current_target(self, elapsed_time):
        total_time = self.ramp_time + self.sustain_time + self.cooldown_time
        
        if elapsed_time > total_time:
            return 0
            
        if elapsed_time <= self.ramp_time:
            progress = elapsed_time / self.ramp_time
            target = int(self.max_concurrent * (math.sin(progress * math.pi / 2)))
        elif elapsed_time <= (self.ramp_time + self.sustain_time):
            target = self.max_concurrent
        else:
            progress = (elapsed_time - self.ramp_time - self.sustain_time) / self.cooldown_time
            target = int(self.max_concurrent * (math.cos(progress * math.pi / 2)))
        
        return max(0, min(target, self.max_concurrent))

    def simulate_connection(self):
        if self.connection_attempts >= self.max_total_connections:
            return

        for attempt in range(self.max_retries):
            if self.shutdown_event.is_set():
                return

            try:
                with self.managed_socket() as sock:
                    target_port = random.choice(self.target_ports)
                    sock.connect(('localhost', target_port))
                    
                    with self.lock:
                        self.current_connections += 1
                        self.connection_attempts += 1
                    
                    while not self.shutdown_event.is_set():
                        try:
                            message = f"GET /resource{random.randint(1,100)} HTTP/1.1\r\nHost: localhost\r\n\r\n"
                            sock.send(message.encode())
                            time.sleep(random.uniform(0.1, 2.0))
                            
                            if random.random() < 0.2:
                                break
                        except socket.error as e:
                            logger.debug(f"Socket error during communication: {e}")
                            break
                    
                    with self.lock:
                        self.current_connections -= 1
                    return
                    
            except (ConnectionRefusedError, socket.error) as e:
                logger.debug(f"Connection attempt {attempt + 1} failed: {e}")
                with self.lock:
                    self.current_connections = max(0, self.current_connections - 1)
                time.sleep(random.uniform(0.1, 0.5))
        
        logger.warning(f"Failed to establish connection after {self.max_retries} attempts")

    def run(self):
        logger.info(f"Starting {self.mode} traffic generation...")
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=self.max_concurrent) as executor:
            while not self.shutdown_event.is_set():
                try:
                    elapsed_time = time.time() - start_time
                    target_connections = self.calculate_current_target(elapsed_time)
                    
                    if elapsed_time >= (self.ramp_time + self.sustain_time + self.cooldown_time):
                        start_time = time.time()
                        continue
                    
                    with self.lock:
                        needed_connections = max(0, target_connections - self.current_connections)
                        if self.connection_attempts >= self.max_total_connections:
                            logger.info("Reached maximum total connections limit")
                            break
                    
                    if needed_connections > 0:
                        for _ in range(needed_connections):
                            if not self.shutdown_event.is_set():
                                executor.submit(self.simulate_connection)
                    
                    logger.info(f"Connections: {self.current_connections}/{target_connections} "
                              f"(Total attempts: {self.connection_attempts})")
                    time.sleep(0.1)
                    
                except Exception as e:
                    logger.error(f"Unexpected error in main loop: {e}")
                    time.sleep(1)
            
            executor.shutdown(wait=True)

def main():
    parser = argparse.ArgumentParser(description='Traffic Generator')
    parser.add_argument('--mode', choices=['normal', 'high'], default='normal',
                      help='Traffic mode: normal or high')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                      default='INFO', help='Logging level')
    
    args = parser.parse_args()
    logging.getLogger().setLevel(getattr(logging, args.log_level))
    
    generator = TrafficGenerator(mode=args.mode)
    generator.run()

if __name__ == "__main__":
    main()