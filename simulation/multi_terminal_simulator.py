#!/usr/bin/env python3
import os
import sys
import time
import random
import curses
import threading
from datetime import datetime

# Import simulator classes
from terminal_simulator import (
    K8sMasterSimulator,
    K8sWorkerSimulator,
    AttackerSimulator,
    CnCServerSimulator,
    DataAggregatorSimulator
)

class MultiTerminalSimulator:
    """
    Simulates multiple terminals in a single window using curses
    """
    def __init__(self):
        self.terminals = {}
        self.active_terminal = None
        self.running = True
        self.stdscr = None
        self.max_y, self.max_x = 0, 0
        self.attack_type = None
        self.target = "192.168.1.100"
        
    def setup_curses(self):
        """Set up the curses environment"""
        self.stdscr = curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        curses.curs_set(0)  # Hide cursor
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        self.stdscr.timeout(100)  # Non-blocking input
        self.max_y, self.max_x = self.stdscr.getmaxyx()
        
        # Define color pairs
        curses.init_pair(1, curses.COLOR_GREEN, -1)  # K8s Master
        curses.init_pair(2, curses.COLOR_BLUE, -1)   # K8s Worker
        curses.init_pair(3, curses.COLOR_RED, -1)    # Attacker
        curses.init_pair(4, curses.COLOR_MAGENTA, -1)  # CnC
        curses.init_pair(5, curses.COLOR_CYAN, -1)   # Data Aggregator
        curses.init_pair(6, curses.COLOR_YELLOW, -1) # Dashboard
        curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_RED)  # Error
        
    def cleanup_curses(self):
        """Clean up curses environment"""
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()
        
    def create_terminal(self, name, simulator_class, hostname=None):
        """Create a new terminal"""
        if hostname is None:
            hostname = name
        
        terminal = simulator_class(hostname)
        self.terminals[name] = {
            "simulator": terminal,
            "buffer": [],
            "max_buffer": 100,
            "color": self._get_color_for_terminal_type(terminal.terminal_type),
            "last_update": datetime.now()
        }
        
        if self.active_terminal is None:
            self.active_terminal = name
            
        return terminal
        
    def _get_color_for_terminal_type(self, terminal_type):
        """Get the color pair for a terminal type"""
        return {
            'k8s-master': 1,
            'k8s-worker': 2,
            'attacker': 3,
            'cnc': 4,
            'data-aggregator': 5,
            'dashboard': 6
        }.get(terminal_type, 0)
        
    def add_log_to_terminal(self, terminal_name, message):
        """Add a log message to a terminal's buffer"""
        if terminal_name in self.terminals:
            terminal = self.terminals[terminal_name]
            buffer = terminal["buffer"]
            
            # Add timestamp to message
            timestamp = datetime.now().strftime("%H:%M:%S")
            full_message = f"[{timestamp}] {message}"
            
            # Add to buffer
            buffer.append(full_message)
            
            # Trim buffer if needed
            if len(buffer) > terminal["max_buffer"]:
                buffer.pop(0)
                
            terminal["last_update"] = datetime.now()
            
    def draw_terminal(self, name, y, x, height, width):
        """Draw a terminal at the specified position"""
        if name not in self.terminals:
            return
            
        terminal = self.terminals[name]
        color = curses.color_pair(terminal["color"])
        is_active = (name == self.active_terminal)
        
        # Draw border
        border_color = color if is_active else curses.color_pair(0)
        for i in range(y, y + height):
            for j in range(x, x + width):
                if i == y or i == y + height - 1 or j == x or j == x + width - 1:
                    try:
                        self.stdscr.addch(i, j, curses.ACS_CKBOARD, border_color)
                    except curses.error:
                        pass
        
        # Draw title
        title = f" {name} "
        title_x = x + (width - len(title)) // 2
        try:
            self.stdscr.addstr(y, title_x, title, color | curses.A_BOLD)
        except curses.error:
            pass
            
        # Draw buffer content
        buffer = terminal["buffer"]
        display_lines = min(len(buffer), height - 2)
        for i in range(display_lines):
            line = buffer[-(display_lines - i)]
            try:
                self.stdscr.addnstr(y + 1 + i, x + 1, line, width - 2, color)
            except curses.error:
                pass
                
    def draw_status_bar(self):
        """Draw the status bar at the bottom of the screen"""
        status = f" Active: {self.active_terminal} | Attack: {self.attack_type or 'None'} | Target: {self.target} | Q: Quit | Tab: Switch | 1-9: Select | A: Attack | S: Stop "
        try:
            self.stdscr.addstr(self.max_y - 1, 0, status.ljust(self.max_x), curses.A_REVERSE)
        except curses.error:
            pass
            
    def handle_input(self):
        """Handle user input"""
        try:
            key = self.stdscr.getch()
            
            if key == ord('q') or key == ord('Q'):
                self.running = False
            elif key == 9:  # Tab
                self._switch_terminal()
            elif key >= ord('1') and key <= ord('9'):
                self._select_terminal_by_number(key - ord('1'))
            elif key == ord('a') or key == ord('A'):
                self._start_attack()
            elif key == ord('s') or key == ord('S'):
                self._stop_attack()
        except Exception as e:
            self._show_error(f"Input error: {e}")
            
    def _switch_terminal(self):
        """Switch to the next terminal"""
        terminal_names = list(self.terminals.keys())
        if not terminal_names:
            return
            
        current_index = terminal_names.index(self.active_terminal) if self.active_terminal in terminal_names else -1
        next_index = (current_index + 1) % len(terminal_names)
        self.active_terminal = terminal_names[next_index]
        
    def _select_terminal_by_number(self, number):
        """Select a terminal by number"""
        terminal_names = list(self.terminals.keys())
        if number < len(terminal_names):
            self.active_terminal = terminal_names[number]
            
    def _start_attack(self):
        """Start an attack simulation"""
        attack_types = ["SYN Flood", "HTTP Flood", "UDP Flood"]
        self.attack_type = random.choice(attack_types)
        
        # Log to CnC terminal
        if "cnc" in self.terminals:
            self.add_log_to_terminal("cnc", f"Starting {self.attack_type} attack against {self.target}")
            self.add_log_to_terminal("cnc", "Sending commands to bots...")
            
        # Log to attacker terminals
        for i in range(1, 4):
            attacker_name = f"attacker{i}"
            if attacker_name in self.terminals:
                self.add_log_to_terminal(attacker_name, f"Received command to execute {self.attack_type} attack")
                self.add_log_to_terminal(attacker_name, f"Target: {self.target}")
                self.add_log_to_terminal(attacker_name, "Launching attack...")
                
        # Log to worker terminals
        for i in range(1, 4):
            worker_name = f"worker{i}"
            if worker_name in self.terminals:
                self.add_log_to_terminal(worker_name, f"High network traffic detected")
                self.add_log_to_terminal(worker_name, f"CPU usage spiking to 85%")
                self.add_log_to_terminal(worker_name, f"Possible {self.attack_type} attack detected")
                
        # Log to master terminal
        if "master" in self.terminals:
            self.add_log_to_terminal("master", "Unusual network activity detected on worker nodes")
            self.add_log_to_terminal("master", "Alerting monitoring system...")
            
        # Log to data aggregator terminal
        if "data-aggregator" in self.terminals:
            self.add_log_to_terminal("data-aggregator", "Receiving high traffic metrics from nodes")
            self.add_log_to_terminal("data-aggregator", "Running anomaly detection...")
            self.add_log_to_terminal("data-aggregator", f"Attack detected: {self.attack_type} (confidence: 97.3%)")
            self.add_log_to_terminal("data-aggregator", "Storing results in InfluxDB...")
            
    def _stop_attack(self):
        """Stop the current attack simulation"""
        if not self.attack_type:
            return
            
        # Log to CnC terminal
        if "cnc" in self.terminals:
            self.add_log_to_terminal("cnc", f"Stopping {self.attack_type} attack")
            self.add_log_to_terminal("cnc", "Sending stop command to bots...")
            
        # Log to attacker terminals
        for i in range(1, 4):
            attacker_name = f"attacker{i}"
            if attacker_name in self.terminals:
                self.add_log_to_terminal(attacker_name, "Received command to stop attack")
                self.add_log_to_terminal(attacker_name, "Attack stopped")
                
        # Log to worker terminals
        for i in range(1, 4):
            worker_name = f"worker{i}"
            if worker_name in self.terminals:
                self.add_log_to_terminal(worker_name, "Network traffic returning to normal")
                self.add_log_to_terminal(worker_name, "CPU usage decreasing")
                
        # Log to master terminal
        if "master" in self.terminals:
            self.add_log_to_terminal("master", "Network activity returning to normal levels")
            
        # Log to data aggregator terminal
        if "data-aggregator" in self.terminals:
            self.add_log_to_terminal("data-aggregator", "Traffic metrics returning to normal")
            self.add_log_to_terminal("data-aggregator", "No anomalies detected in recent data")
            
        self.attack_type = None
        
    def _show_error(self, message):
        """Show an error message"""
        try:
            self.stdscr.addstr(0, 0, f"ERROR: {message}", curses.color_pair(7) | curses.A_BOLD)
            self.stdscr.refresh()
            time.sleep(2)
        except curses.error:
            pass
            
    def run(self):
        """Run the multi-terminal simulator"""
        try:
            self.setup_curses()
            
            # Create terminals
            self.create_terminal("master", K8sMasterSimulator, "k8s-master-01")
            for i in range(1, 4):
                self.create_terminal(f"worker{i}", K8sWorkerSimulator, f"k8s-worker-{i:02d}")
            self.create_terminal("cnc", CnCServerSimulator, "cnc-server")
            for i in range(1, 4):
                self.create_terminal(f"attacker{i}", AttackerSimulator, f"attacker-{i:02d}")
            self.create_terminal("data-aggregator", DataAggregatorSimulator, "data-aggregator")
            
            # Add initial logs
            self.add_log_to_terminal("master", "Kubernetes cluster is running")
            self.add_log_to_terminal("master", "All nodes are healthy")
            
            for i in range(1, 4):
                self.add_log_to_terminal(f"worker{i}", "Node started and joined the cluster")
                self.add_log_to_terminal(f"worker{i}", "Running system checks...")
                self.add_log_to_terminal(f"worker{i}", "All services operational")
                
            self.add_log_to_terminal("cnc", "Command and Control server initialized")
            self.add_log_to_terminal("cnc", "Connected to 3 bots")
            
            for i in range(1, 4):
                self.add_log_to_terminal(f"attacker{i}", "Bot initialized")
                self.add_log_to_terminal(f"attacker{i}", "Connected to CnC server")
                self.add_log_to_terminal(f"attacker{i}", "Waiting for commands...")
                
            self.add_log_to_terminal("data-aggregator", "Data aggregator service started")
            self.add_log_to_terminal("data-aggregator", "Connected to InfluxDB")
            self.add_log_to_terminal("data-aggregator", "Waiting for metrics from nodes...")
            
            # Main loop
            while self.running:
                self.stdscr.clear()
                
                # Calculate terminal positions
                term_height = (self.max_y - 1) // 3
                term_width = self.max_x // 3
                
                # Draw terminals
                positions = {
                    "master": (0, 0),
                    "worker1": (0, term_width),
                    "worker2": (0, term_width * 2),
                    "worker3": (term_height, 0),
                    "cnc": (term_height, term_width),
                    "data-aggregator": (term_height, term_width * 2),
                    "attacker1": (term_height * 2, 0),
                    "attacker2": (term_height * 2, term_width),
                    "attacker3": (term_height * 2, term_width * 2)
                }
                
                for name, (y, x) in positions.items():
                    self.draw_terminal(name, y, x, term_height, term_width)
                    
                self.draw_status_bar()
                self.stdscr.refresh()
                self.handle_input()
                
                # Simulate random logs
                if random.random() < 0.1:  # 10% chance each iteration
                    self._simulate_random_log()
                    
                time.sleep(0.1)
                
        except Exception as e:
            self.cleanup_curses()
            print(f"Error: {e}")
        finally:
            self.cleanup_curses()
            
    def _simulate_random_log(self):
        """Add a random log message to a random terminal"""
        terminal_name = random.choice(list(self.terminals.keys()))
        terminal_type = self.terminals[terminal_name]["simulator"].terminal_type
        
        logs = {
            'k8s-master': [
                "Checking node status...",
                "All pods are running",
                "API server is healthy",
                "Scheduler is operational",
                "Controller manager is running"
            ],
            'k8s-worker': [
                "Running container health checks",
                "Monitoring system resources",
                "Network traffic normal",
                "Storage subsystem healthy",
                "Kubelet status: OK"
            ],
            'attacker': [
                "Scanning for targets...",
                "Checking connection to CnC",
                "Resources available for attack",
                "Waiting for next command",
                "System ready"
            ],
            'cnc': [
                "Monitoring bot status",
                "All bots connected",
                "System ready for commands",
                "Checking target availability",
                "Preparing attack vectors"
            ],
            'data-aggregator': [
                "Processing metrics data",
                "Running anomaly detection",
                "Model inference complete",
                "Storing results in database",
                "Checking for new data"
            ]
        }
        
        if terminal_type in logs:
            message = random.choice(logs[terminal_type])
            self.add_log_to_terminal(terminal_name, message)

def main():
    simulator = MultiTerminalSimulator()
    simulator.run()

if __name__ == "__main__":
    main() 