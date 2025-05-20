#!/usr/bin/env python3
import curses
import time
import random
from datetime import datetime, timedelta

class DashboardUI:
    """
    Terminal-based dashboard UI for DoS detection system
    """
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN, -1)  # Normal
        curses.init_pair(2, curses.COLOR_YELLOW, -1)  # Warning
        curses.init_pair(3, curses.COLOR_RED, -1)     # Critical
        curses.init_pair(4, curses.COLOR_CYAN, -1)    # Info
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLUE)  # Header
        self.stdscr.clear()
        self.height, self.width = self.stdscr.getmaxyx()
        self.attack_in_progress = False
        self.attack_type = None
        self.attack_start_time = None
        self.attack_duration = 0
        self.detection_time = None
        
    def draw_header(self):
        """Draw the dashboard header"""
        header = "KUBERNETES DOS DETECTION SYSTEM DASHBOARD"
        self.stdscr.attron(curses.color_pair(5))
        self.stdscr.addstr(0, 0, " " * self.width)
        self.stdscr.addstr(0, (self.width - len(header)) // 2, header)
        self.stdscr.attroff(curses.color_pair(5))
        
        # Draw time
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.stdscr.addstr(1, self.width - len(now) - 2, now)
        
    def draw_cluster_status(self, y_start):
        """Draw the cluster status panel"""
        self.draw_panel_header(y_start, "CLUSTER STATUS")
        
        nodes = [
            ("k8s-master-01", "Ready", "Control-Plane", "45d", "v1.26.3", 1),
            ("k8s-worker-01", "Ready", "Worker", "45d", "v1.26.3", 1),
            ("k8s-worker-02", "Ready", "Worker", "45d", "v1.26.3", 1 if not self.attack_in_progress else 3),
            ("k8s-worker-03", "Ready", "Worker", "45d", "v1.26.3", 1)
        ]
        
        # Draw table header
        self.stdscr.addstr(y_start + 2, 2, "NODE NAME")
        self.stdscr.addstr(y_start + 2, 20, "STATUS")
        self.stdscr.addstr(y_start + 2, 35, "ROLE")
        self.stdscr.addstr(y_start + 2, 50, "AGE")
        self.stdscr.addstr(y_start + 2, 60, "VERSION")
        
        # Draw separator
        self.stdscr.addstr(y_start + 3, 2, "-" * (self.width - 4))
        
        # Draw nodes
        for i, (name, status, role, age, version, color) in enumerate(nodes):
            self.stdscr.attron(curses.color_pair(color))
            self.stdscr.addstr(y_start + 4 + i, 2, name)
            self.stdscr.addstr(y_start + 4 + i, 20, status)
            self.stdscr.addstr(y_start + 4 + i, 35, role)
            self.stdscr.addstr(y_start + 4 + i, 50, age)
            self.stdscr.addstr(y_start + 4 + i, 60, version)
            self.stdscr.attroff(curses.color_pair(color))
            
        return y_start + 4 + len(nodes) + 1
        
    def draw_network_traffic(self, y_start):
        """Draw the network traffic panel"""
        self.draw_panel_header(y_start, "NETWORK TRAFFIC")
        
        # Draw chart axes
        chart_width = self.width - 20
        chart_height = 8
        
        # Draw y-axis
        for i in range(chart_height):
            self.stdscr.addstr(y_start + 2 + chart_height - i, 2, f"{i*10:3d} |")
            
        # Draw x-axis
        self.stdscr.addstr(y_start + 2 + chart_height + 1, 7, "+" + "-" * chart_width)
        
        # Draw time labels
        now = datetime.now()
        for i in range(5):
            time_label = (now - timedelta(minutes=(4-i)*5)).strftime("%H:%M")
            pos = 7 + int(i * chart_width / 4)
            self.stdscr.addstr(y_start + 2 + chart_height + 2, pos, time_label)
            
        # Draw traffic data
        if not self.attack_in_progress:
            # Normal traffic pattern
            traffic_data = [random.randint(5, 15) for _ in range(chart_width)]
        else:
            # Attack traffic pattern
            if self.attack_type == "SYN Flood":
                # Simulate SYN flood pattern
                traffic_data = [random.randint(5, 15) if i < chart_width // 2 else 
                               random.randint(60, 80) for i in range(chart_width)]
            elif self.attack_type == "HTTP Flood":
                # Simulate HTTP flood pattern
                traffic_data = [random.randint(5, 15) if i < chart_width // 2 else 
                               random.randint(40, 60) for i in range(chart_width)]
            else:
                # Generic attack pattern
                traffic_data = [random.randint(5, 15) if i < chart_width // 2 else 
                               random.randint(50, 70) for i in range(chart_width)]
        
        # Plot the traffic data
        for i, value in enumerate(traffic_data):
            if i >= chart_width:
                break
                
            # Scale the value to fit in chart_height
            scaled_value = min(int(value * chart_height / 80), chart_height)
            
            # Determine color based on value
            color = 1 if value < 30 else (2 if value < 60 else 3)
            
            # Draw the point
            self.stdscr.attron(curses.color_pair(color))
            if i > 0 and i < len(traffic_data) - 1:
                self.stdscr.addstr(y_start + 2 + chart_height - scaled_value, 7 + i, "*")
            self.stdscr.attroff(curses.color_pair(color))
            
        return y_start + 2 + chart_height + 3
        
    def draw_detection_status(self, y_start):
        """Draw the attack detection status panel"""
        self.draw_panel_header(y_start, "ATTACK DETECTION STATUS")
        
        if not self.attack_in_progress:
            self.stdscr.attron(curses.color_pair(1))
            self.stdscr.addstr(y_start + 2, 2, "STATUS: No attacks detected")
            self.stdscr.attroff(curses.color_pair(1))
            self.stdscr.addstr(y_start + 3, 2, "Last scan: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        else:
            # Attack is in progress
            self.stdscr.attron(curses.color_pair(3))
            self.stdscr.addstr(y_start + 2, 2, f"STATUS: ATTACK DETECTED - {self.attack_type}")
            self.stdscr.attroff(curses.color_pair(3))
            
            # Show attack details
            self.stdscr.addstr(y_start + 3, 2, f"Attack start: {self.attack_start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            self.stdscr.addstr(y_start + 4, 2, f"Detection time: {self.detection_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Calculate detection delay
            detection_delay = (self.detection_time - self.attack_start_time).total_seconds()
            self.stdscr.addstr(y_start + 5, 2, f"Detection delay: {detection_delay:.2f} seconds")
            
            # Show confidence score
            confidence = random.uniform(95.0, 99.9)
            self.stdscr.addstr(y_start + 6, 2, f"Confidence score: {confidence:.2f}%")
            
            # Show affected nodes
            self.stdscr.addstr(y_start + 7, 2, "Affected nodes: k8s-worker-02")
            
            # Show model predictions
            self.stdscr.addstr(y_start + 9, 2, "MODEL PREDICTIONS:")
            self.stdscr.addstr(y_start + 10, 4, f"RandomForest: {self.attack_type} ({random.uniform(96.0, 99.0):.2f}%)")
            self.stdscr.addstr(y_start + 11, 4, f"LSTM: {self.attack_type} ({random.uniform(95.0, 99.0):.2f}%)")
            self.stdscr.addstr(y_start + 12, 4, f"CNN: {self.attack_type} ({random.uniform(96.0, 99.0):.2f}%)")
            
        return y_start + 14
        
    def draw_system_metrics(self, y_start):
        """Draw system metrics panel"""
        self.draw_panel_header(y_start, "SYSTEM METRICS")
        
        # CPU usage
        self.stdscr.addstr(y_start + 2, 2, "CPU Usage:")
        cpu_values = {
            "k8s-master-01": 25,
            "k8s-worker-01": 30,
            "k8s-worker-02": 85 if self.attack_in_progress else 35,
            "k8s-worker-03": 28
        }
        
        for i, (node, value) in enumerate(cpu_values.items()):
            color = 1 if value < 60 else (2 if value < 80 else 3)
            bar_length = int(value * (self.width - 30) / 100)
            self.stdscr.addstr(y_start + 3 + i, 4, f"{node}: ")
            self.stdscr.addstr(y_start + 3 + i, 20, f"{value:3d}% ")
            self.stdscr.attron(curses.color_pair(color))
            self.stdscr.addstr(y_start + 3 + i, 25, "█" * bar_length)
            self.stdscr.attroff(curses.color_pair(color))
            
        # Memory usage
        self.stdscr.addstr(y_start + 8, 2, "Memory Usage:")
        mem_values = {
            "k8s-master-01": 40,
            "k8s-worker-01": 45,
            "k8s-worker-02": 75 if self.attack_in_progress else 48,
            "k8s-worker-03": 42
        }
        
        for i, (node, value) in enumerate(mem_values.items()):
            color = 1 if value < 60 else (2 if value < 80 else 3)
            bar_length = int(value * (self.width - 30) / 100)
            self.stdscr.addstr(y_start + 9 + i, 4, f"{node}: ")
            self.stdscr.addstr(y_start + 9 + i, 20, f"{value:3d}% ")
            self.stdscr.attron(curses.color_pair(color))
            self.stdscr.addstr(y_start + 9 + i, 25, "█" * bar_length)
            self.stdscr.attroff(curses.color_pair(color))
            
        return y_start + 14
        
    def draw_alert_log(self, y_start):
        """Draw alert log panel"""
        self.draw_panel_header(y_start, "ALERT LOG")
        
        alerts = []
        now = datetime.now()
        
        if self.attack_in_progress:
            # Add attack-related alerts
            detection_time_str = self.detection_time.strftime("%H:%M:%S")
            alerts = [
                (f"{detection_time_str}", "CRITICAL", f"{self.attack_type} attack detected on k8s-worker-02", 3),
                (f"{(self.detection_time - timedelta(seconds=2)).strftime('%H:%M:%S')}", "WARNING", "Unusual network traffic pattern detected", 2),
                (f"{(self.detection_time - timedelta(seconds=5)).strftime('%H:%M:%S')}", "WARNING", "High CPU usage on k8s-worker-02", 2),
                (f"{(self.detection_time - timedelta(seconds=10)).strftime('%H:%M:%S')}", "INFO", "Model inference started for anomaly detection", 4)
            ]
        
        # Add some normal operational alerts
        alerts.extend([
            ((now - timedelta(minutes=5)).strftime("%H:%M:%S"), "INFO", "Routine security scan completed", 4),
            ((now - timedelta(minutes=15)).strftime("%H:%M:%S"), "INFO", "System metrics collected successfully", 4),
            ((now - timedelta(minutes=30)).strftime("%H:%M:%S"), "INFO", "Models updated with latest training data", 4)
        ])
        
        # Draw alerts
        for i, (time_str, level, message, color) in enumerate(alerts):
            if i >= 10:  # Limit to 10 alerts
                break
                
            self.stdscr.addstr(y_start + 2 + i, 2, time_str)
            self.stdscr.attron(curses.color_pair(color))
            self.stdscr.addstr(y_start + 2 + i, 12, f"[{level}]")
            self.stdscr.attroff(curses.color_pair(color))
            self.stdscr.addstr(y_start + 2 + i, 25, message)
            
        return y_start + 2 + len(alerts) + 1
        
    def draw_panel_header(self, y, title):
        """Draw a panel header"""
        self.stdscr.addstr(y, 0, "┌" + "─" * (self.width - 2) + "┐")
        self.stdscr.addstr(y, 2, f" {title} ")
        
    def simulate_attack(self, attack_type="SYN Flood", duration=60):
        """Simulate an attack"""
        self.attack_in_progress = True
        self.attack_type = attack_type
        self.attack_start_time = datetime.now()
        self.attack_duration = duration
        
        # Simulate detection delay (between 3-10 seconds)
        detection_delay = random.uniform(3, 10)
        self.detection_time = self.attack_start_time + timedelta(seconds=detection_delay)
        
    def stop_attack(self):
        """Stop the simulated attack"""
        self.attack_in_progress = False
        self.attack_type = None
        self.attack_start_time = None
        self.detection_time = None
        
    def update(self):
        """Update the dashboard"""
        self.stdscr.clear()
        self.draw_header()
        
        y_pos = 2
        y_pos = self.draw_cluster_status(y_pos)
        y_pos = self.draw_network_traffic(y_pos)
        
        # Split the bottom section into two columns
        left_width = self.width // 2
        
        # Save current y position
        y_start_bottom = y_pos
        
        # Draw detection status on left
        self.draw_detection_status(y_pos)
        
        # Draw system metrics on right
        self.draw_system_metrics(y_pos)
        
        # Draw alert log at the bottom
        bottom_y = y_start_bottom + 15
        self.draw_alert_log(bottom_y)
        
        # Draw footer
        footer = "Press 'q' to quit, 'a' to simulate attack, 's' to stop attack"
        self.stdscr.addstr(self.height - 1, 0, footer)
        
        self.stdscr.refresh()

def main(stdscr):
    """Main function"""
    curses.curs_set(0)  # Hide cursor
    dashboard = DashboardUI(stdscr)
    
    # Set up key handling
    stdscr.nodelay(True)
    stdscr.timeout(100)
    
    # Main loop
    running = True
    while running:
        # Update the dashboard
        dashboard.update()
        
        # Handle key presses
        try:
            key = stdscr.getch()
            if key == ord('q'):
                running = False
            elif key == ord('a'):
                # Simulate attack
                attack_types = ["SYN Flood", "HTTP Flood", "UDP Flood"]
                dashboard.simulate_attack(random.choice(attack_types))
            elif key == ord('s'):
                # Stop attack
                dashboard.stop_attack()
        except:
            pass
            
        time.sleep(0.1)

if __name__ == "__main__":
    curses.wrapper(main) 