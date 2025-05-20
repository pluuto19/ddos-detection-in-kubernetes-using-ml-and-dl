#!/usr/bin/env python3
import os
import time
import random
import curses
import threading
from datetime import datetime

class TerminalSimulator:
    """
    Simulates different terminals for the K8s infrastructure demo
    """
    def __init__(self, terminal_type, hostname):
        self.terminal_type = terminal_type
        self.hostname = hostname
        self.log_buffer = []
        self.max_buffer_size = 100
        self.prompt_color = {
            'k8s-master': '\033[1;32m',  # Green
            'k8s-worker': '\033[1;34m',  # Blue
            'attacker': '\033[1;31m',    # Red
            'cnc': '\033[1;35m',         # Purple
            'data-aggregator': '\033[1;36m',  # Cyan
            'dashboard': '\033[1;33m'    # Yellow
        }.get(terminal_type, '\033[1;37m')  # Default white
        
        self.reset_color = '\033[0m'
        
    def get_prompt(self):
        """Returns a terminal prompt based on the terminal type"""
        user = {
            'k8s-master': 'root',
            'k8s-worker': 'kube',
            'attacker': 'attacker',
            'cnc': 'admin',
            'data-aggregator': 'datauser',
            'dashboard': 'dashboard'
        }.get(self.terminal_type, 'user')
        
        return f"{self.prompt_color}{user}@{self.hostname}:~$ {self.reset_color}"
    
    def add_log(self, message, delay=0.05):
        """Adds a log message to the buffer with typing effect"""
        if len(self.log_buffer) >= self.max_buffer_size:
            self.log_buffer.pop(0)
        
        # Print with typing effect
        print(self.get_prompt(), end='', flush=True)
        for char in message:
            print(char, end='', flush=True)
            time.sleep(delay * random.uniform(0.5, 1.5))
        print()
        
        # Add to buffer
        self.log_buffer.append(message)
        
    def run_command(self, command, output_lines=None, delay=0.05, cmd_delay=1.0):
        """Simulates running a command with output"""
        self.add_log(command, delay)
        time.sleep(cmd_delay)  # Simulate command execution time
        
        if output_lines:
            for line in output_lines:
                print(line)
                time.sleep(delay * 2)
                self.log_buffer.append(line)
                
    def clear_screen(self):
        """Clears the terminal screen"""
        os.system('clear')
        
    def show_header(self):
        """Shows a header with terminal information"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header = f"=== {self.terminal_type.upper()} TERMINAL ({self.hostname}) - {now} ===\n"
        print(self.prompt_color + header + self.reset_color)

class K8sMasterSimulator(TerminalSimulator):
    """Simulates a Kubernetes master node terminal"""
    def __init__(self, hostname="k8s-master-01"):
        super().__init__("k8s-master", hostname)
        
    def show_cluster_status(self):
        self.run_command("kubectl get nodes", [
            "NAME            STATUS   ROLES           AGE    VERSION",
            "k8s-master-01   Ready    control-plane   45d    v1.26.3",
            "k8s-worker-01   Ready    worker          45d    v1.26.3",
            "k8s-worker-02   Ready    worker          45d    v1.26.3",
            "k8s-worker-03   Ready    worker          45d    v1.26.3"
        ])
        
    def show_pods(self):
        self.run_command("kubectl get pods -A", [
            "NAMESPACE     NAME                                      READY   STATUS    RESTARTS   AGE",
            "kube-system   coredns-787d4945fb-9vs6m                  1/1     Running   0          45d",
            "kube-system   etcd-k8s-master-01                        1/1     Running   0          45d",
            "kube-system   kube-apiserver-k8s-master-01              1/1     Running   0          45d",
            "kube-system   kube-controller-manager-k8s-master-01     1/1     Running   0          45d",
            "kube-system   kube-proxy-5xkrb                          1/1     Running   0          45d",
            "kube-system   kube-scheduler-k8s-master-01              1/1     Running   0          45d",
            "monitoring    node-exporter-scraper-5f7d9b4f5d-jk2l7    1/1     Running   0          30d",
            "monitoring    falco-scraper-7d8f9c8b5c-2xvnp            1/1     Running   0          30d",
            "monitoring    agent-controller-6b7d8c9f7b-x2vnq         1/1     Running   0          30d"
        ])
        
    def show_services(self):
        self.run_command("kubectl get services -A", [
            "NAMESPACE     NAME                  TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                  AGE",
            "default       kubernetes            ClusterIP   10.96.0.1        <none>        443/TCP                  45d",
            "kube-system   kube-dns              ClusterIP   10.96.0.10       <none>        53/UDP,53/TCP,9153/TCP   45d",
            "monitoring    node-exporter-svc     ClusterIP   10.100.200.123   <none>        9100/TCP                 30d",
            "monitoring    falco-scraper-svc     ClusterIP   10.100.200.124   <none>        8765/TCP                 30d"
        ])
        
    def show_agent_logs(self):
        self.run_command("kubectl logs -n monitoring agent-controller-6b7d8c9f7b-x2vnq --tail=5", [
            "2023-06-15T10:23:45Z INFO  agent-controller - Collecting metrics from node-exporter",
            "2023-06-15T10:23:45Z INFO  agent-controller - Collecting events from falco",
            "2023-06-15T10:23:46Z INFO  agent-controller - Sending 128 metrics to data aggregator",
            "2023-06-15T10:23:46Z INFO  agent-controller - Successfully sent data",
            "2023-06-15T10:23:50Z INFO  agent-controller - Detected unusual network traffic on worker-02"
        ])

class K8sWorkerSimulator(TerminalSimulator):
    """Simulates a Kubernetes worker node terminal"""
    def __init__(self, hostname="k8s-worker-01"):
        super().__init__("k8s-worker", hostname)
        
    def show_system_info(self):
        self.run_command("top -n 1", [
            "top - 10:24:15 up 45 days,  2:03,  1 user,  load average: 0.52, 0.58, 0.59",
            "Tasks: 128 total,   1 running, 127 sleeping,   0 stopped,   0 zombie",
            "%Cpu(s):  5.9 us,  2.1 sy,  0.0 ni, 91.7 id,  0.1 wa,  0.0 hi,  0.2 si,  0.0 st",
            "MiB Mem :   7950.8 total,   2341.2 free,   3218.5 used,   2391.1 buff/cache",
            "MiB Swap:   2048.0 total,   2048.0 free,      0.0 used.   4392.5 avail Mem"
        ])
        
    def show_network_traffic(self):
        self.run_command("netstat -tuln | grep LISTEN", [
            "tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN",
            "tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN",
            "tcp        0      0 0.0.0.0:9100            0.0.0.0:*               LISTEN",
            "tcp6       0      0 :::10250                :::*                    LISTEN",
            "tcp6       0      0 :::22                   :::*                    LISTEN"
        ])
        
    def show_agent_status(self):
        self.run_command("systemctl status node-exporter", [
            "● node-exporter.service - Prometheus Node Exporter",
            "     Loaded: loaded (/etc/systemd/system/node-exporter.service; enabled; vendor preset: enabled)",
            "     Active: active (running) since Mon 2023-05-01 08:15:23 UTC; 45 days ago",
            "   Main PID: 1234 (node_exporter)",
            "      Tasks: 6 (limit: 4915)",
            "     Memory: 14.2M",
            "        CPU: 45min 23.432s"
        ])
        
    def show_under_attack(self, attack_type="SYN Flood"):
        self.run_command(f"dmesg | grep -i drop", [
            f"[12345.123456] kernel: TCP: request_sock_TCP: Possible {attack_type} attack detected",
            f"[12345.123556] kernel: TCP: Dropping 1254 packets due to overload",
            f"[12345.123656] kernel: net_ratelimit: 35 callbacks suppressed",
            f"[12345.123756] kernel: TCP: Dropping SYN from 192.168.10.123: synflood is detected"
        ])
        
        self.run_command("netstat -s | grep -i drop", [
            "    1254 SYNs to LISTEN sockets dropped",
            "    3421 packets dropped",
            "    156 dropped because of missing route"
        ])

class AttackerSimulator(TerminalSimulator):
    """Simulates an attacker node terminal"""
    def __init__(self, hostname="attacker-01"):
        super().__init__("attacker", hostname)
        
    def show_attack_preparation(self, target="192.168.1.100", attack_type="SYN Flood"):
        self.run_command(f"ping -c 3 {target}", [
            f"PING {target} ({target}) 56(84) bytes of data.",
            f"64 bytes from {target}: icmp_seq=1 ttl=64 time=0.345 ms",
            f"64 bytes from {target}: icmp_seq=2 ttl=64 time=0.401 ms", 
            f"64 bytes from {target}: icmp_seq=3 ttl=64 time=0.378 ms",
            f"",
            f"--- {target} ping statistics ---",
            f"3 packets transmitted, 3 received, 0% packet loss, time 2046ms",
            f"rtt min/avg/max/mdev = 0.345/0.374/0.401/0.028 ms"
        ])
        
    def launch_attack(self, target="192.168.1.100", attack_type="SYN Flood", duration=30):
        if attack_type == "SYN Flood":
            self.run_command(f"./attack.py --type syn_flood --target {target} --duration {duration}", [
                f"[*] Preparing SYN Flood attack against {target}",
                f"[*] Attack parameters: threads=8, packets_per_second=10000",
                f"[*] Starting attack for {duration} seconds...",
                f"[*] Sending SYN packets...",
                f"[*] Progress: ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 100%",
                f"[*] Attack completed. Sent 300000 packets."
            ])
        elif attack_type == "HTTP Flood":
            self.run_command(f"./attack.py --type http_flood --target {target} --duration {duration}", [
                f"[*] Preparing HTTP Flood attack against {target}",
                f"[*] Attack parameters: threads=16, requests_per_second=5000",
                f"[*] Starting attack for {duration} seconds...",
                f"[*] Sending HTTP requests...",
                f"[*] Progress: ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 100%",
                f"[*] Attack completed. Sent 150000 requests."
            ])
        elif attack_type == "UDP Flood":
            self.run_command(f"./attack.py --type udp_flood --target {target} --duration {duration}", [
                f"[*] Preparing UDP Flood attack against {target}",
                f"[*] Attack parameters: threads=8, packets_per_second=15000",
                f"[*] Starting attack for {duration} seconds...",
                f"[*] Sending UDP packets...",
                f"[*] Progress: ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 100%",
                f"[*] Attack completed. Sent 450000 packets."
            ])

class CnCServerSimulator(TerminalSimulator):
    """Simulates a Command and Control server terminal"""
    def __init__(self, hostname="cnc-server"):
        super().__init__("cnc", hostname)
        self.bots = ["attacker-01", "attacker-02", "attacker-03"]
        
    def show_bot_list(self):
        self.run_command("./botnet.py list", [
            "=== Available Bots ===",
            "ID    | Hostname    | IP Address      | Status  | Last Seen",
            "------+-------------+-----------------+---------+----------------",
            "001   | attacker-01 | 192.168.10.101  | ONLINE  | 2023-06-15 10:20:15",
            "002   | attacker-02 | 192.168.10.102  | ONLINE  | 2023-06-15 10:19:45",
            "003   | attacker-03 | 192.168.10.103  | ONLINE  | 2023-06-15 10:21:02"
        ])
        
    def issue_attack_command(self, attack_type="SYN Flood", target="192.168.1.100", duration=30):
        self.run_command(f"./botnet.py attack --type {attack_type} --target {target} --duration {duration} --bots all", [
            f"[*] Sending attack command to all bots",
            f"[*] Attack type: {attack_type}",
            f"[*] Target: {target}",
            f"[*] Duration: {duration} seconds",
            f"[*] Command sent successfully to 3 bots",
            f"[*] Bot attacker-01: Acknowledged",
            f"[*] Bot attacker-02: Acknowledged", 
            f"[*] Bot attacker-03: Acknowledged",
            f"[*] Attack started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        ])
        
    def show_attack_status(self):
        self.run_command("./botnet.py status", [
            "=== Active Attacks ===",
            "Target: 192.168.1.100 | Type: SYN Flood | Progress: 75% | Bots: 3/3",
            "",
            "=== Bot Status ===",
            "attacker-01: ATTACKING | Packets Sent: 225000 | CPU: 78% | MEM: 45%",
            "attacker-02: ATTACKING | Packets Sent: 227500 | CPU: 82% | MEM: 43%",
            "attacker-03: ATTACKING | Packets Sent: 221000 | CPU: 76% | MEM: 42%"
        ])

class DataAggregatorSimulator(TerminalSimulator):
    """Simulates a data aggregator server terminal"""
    def __init__(self, hostname="data-aggregator"):
        super().__init__("data-aggregator", hostname)
        
    def show_data_collection(self):
        self.run_command("python3 data_aggregator.py --status", [
            "=== Data Aggregator Status ===",
            "Status: Running",
            "Uptime: 5 days, 7 hours, 23 minutes",
            "Connected agents: 3",
            "Database connection: OK",
            "Model service: OK",
            "",
            "=== Recent Data Collection ===",
            "Last collection: 2023-06-15 10:24:30",
            "Metrics collected: 384",
            "Events collected: 56",
            "Storage usage: 45.7 GB / 500.0 GB"
        ])
        
    def show_data_processing(self):
        self.run_command("python3 data_aggregator.py --process", [
            "[INFO] Starting data processing...",
            "[INFO] Loading system metrics from agents...",
            "[INFO] Processing network traffic data...",
            "[INFO] Detected anomaly in network traffic patterns",
            "[INFO] Running inference on collected data...",
            "[INFO] Model prediction: SYN Flood attack detected (confidence: 97.8%)",
            "[INFO] Storing results in database...",
            "[INFO] Results stored successfully",
            "[INFO] Sending alert to dashboard..."
        ])
        
    def show_model_inference(self):
        self.run_command("python3 data_aggregator.py --inference --latest", [
            "[INFO] Loading latest data for inference...",
            "[INFO] Preparing features for model input...",
            "[INFO] Running inference with RandomForest model...",
            "[INFO] Running inference with LSTM model...",
            "[INFO] Running inference with CNN model...",
            "[INFO] Model predictions:",
            "       - RandomForest: SYN Flood (confidence: 97.8%)",
            "       - LSTM: SYN Flood (confidence: 96.5%)",
            "       - CNN: SYN Flood (confidence: 98.2%)",
            "[INFO] Ensemble prediction: SYN Flood (confidence: 97.5%)",
            "[INFO] Storing prediction in database..."
        ])

class DashboardSimulator(TerminalSimulator):
    """Simulates a dashboard terminal"""
    def __init__(self, hostname="dashboard"):
        super().__init__("dashboard", hostname)
        
    def start_dashboard(self):
        self.run_command("python3 dashboard.py", [
            "[INFO] Starting dashboard server...",
            "[INFO] Connecting to InfluxDB...",
            "[INFO] Connection successful",
            "[INFO] Loading ML models...",
            "[INFO] Models loaded successfully",
            "[INFO] Dashboard running at http://localhost:3000"
        ])
        
    def show_dashboard_logs(self):
        self.run_command("tail -f dashboard.log", [
            "2023-06-15 10:24:00 INFO - User admin logged in",
            "2023-06-15 10:24:15 INFO - Fetching latest metrics from database",
            "2023-06-15 10:24:16 INFO - Rendering dashboard with 3 active panels",
            "2023-06-15 10:24:30 INFO - Received new data from aggregator",
            "2023-06-15 10:24:31 WARN - Anomaly detected in worker-02 metrics",
            "2023-06-15 10:24:32 ALERT - Attack detected: SYN Flood (confidence: 97.5%)",
            "2023-06-15 10:24:33 INFO - Updating dashboard visualizations",
            "2023-06-15 10:24:34 INFO - Alert notification sent to admin"
        ])

def main():
    """Main function to demonstrate the terminal simulators"""
    # Create instances of each simulator
    master = K8sMasterSimulator()
    worker1 = K8sWorkerSimulator("k8s-worker-01")
    worker2 = K8sWorkerSimulator("k8s-worker-02")
    worker3 = K8sWorkerSimulator("k8s-worker-03")
    attacker1 = AttackerSimulator("attacker-01")
    attacker2 = AttackerSimulator("attacker-02")
    attacker3 = AttackerSimulator("attacker-03")
    cnc = CnCServerSimulator()
    data_agg = DataAggregatorSimulator()
    dashboard = DashboardSimulator()
    
    # Example usage
    master.clear_screen()
    master.show_header()
    master.show_cluster_status()
    master.show_pods()
    
    # You would implement a UI to switch between terminals
    # and orchestrate the demo flow here

if __name__ == "__main__":
    main() 