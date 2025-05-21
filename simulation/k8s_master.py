#!/usr/bin/env python3
import os
import time
import random
from datetime import datetime

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the terminal header"""
    print("=" * 60)
    print("KUBERNETES MASTER NODE (k8s-master-01)")
    print("=" * 60)
    print()

def simulate_k8s_master():
    """Simulate the Kubernetes master node"""
    clear_screen()
    print_header()
    
    while True:
        try:
            # Show cluster status
            print("\n[{}] Checking cluster status...".format(datetime.now().strftime("%H:%M:%S")))
            time.sleep(1)
            
            print("\nNODE STATUS:")
            print("NAME            STATUS   ROLES           AGE    VERSION")
            print("k8s-master-01   Ready    control-plane   45d    v1.26.3")
            print("k8s-worker-01   Ready    worker          45d    v1.26.3")
            print("k8s-worker-02   Ready    worker          45d    v1.26.3")
            print("k8s-worker-03   Ready    worker          45d    v1.26.3")
            
            time.sleep(3)
            
            # Show pods
            print("\n[{}] Checking pods...".format(datetime.now().strftime("%H:%M:%S")))
            time.sleep(1)
            
            print("\nPODS STATUS:")
            print("NAMESPACE     NAME                                      READY   STATUS    RESTARTS   AGE")
            print("kube-system   coredns-787d4945fb-9vs6m                  1/1     Running   0          45d")
            print("kube-system   etcd-k8s-master-01                        1/1     Running   0          45d")
            print("kube-system   kube-apiserver-k8s-master-01              1/1     Running   0          45d")
            print("kube-system   kube-controller-manager-k8s-master-01     1/1     Running   0          45d")
            print("kube-system   kube-proxy-5xkrb                          1/1     Running   0          45d")
            print("kube-system   kube-scheduler-k8s-master-01              1/1     Running   0          45d")
            print("monitoring    node-exporter-scraper-5f7d9b4f5d-jk2l7    1/1     Running   0          30d")
            print("monitoring    falco-scraper-7d8f9c8b5c-2xvnp            1/1     Running   0          30d")
            print("monitoring    agent-controller-6b7d8c9f7b-x2vnq         1/1     Running   0          30d")
            
            time.sleep(3)
            
            # Show services
            print("\n[{}] Checking services...".format(datetime.now().strftime("%H:%M:%S")))
            time.sleep(1)
            
            print("\nSERVICES STATUS:")
            print("NAMESPACE     NAME                  TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)")
            print("default       kubernetes            ClusterIP   10.96.0.1        <none>        443/TCP")
            print("kube-system   kube-dns              ClusterIP   10.96.0.10       <none>        53/UDP,53/TCP")
            print("monitoring    node-exporter-svc     ClusterIP   10.100.200.123   <none>        9100/TCP")
            print("monitoring    falco-scraper-svc     ClusterIP   10.100.200.124   <none>        8765/TCP")
            
            time.sleep(3)
            
            # Show agent logs
            print("\n[{}] Checking agent logs...".format(datetime.now().strftime("%H:%M:%S")))
            time.sleep(1)
            
            print("\nAGENT LOGS:")
            current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            print(f"{current_time} INFO  agent-controller - Collecting metrics from node-exporter")
            print(f"{current_time} INFO  agent-controller - Collecting events from falco")
            print(f"{current_time} INFO  agent-controller - Sending 128 metrics to data aggregator")
            print(f"{current_time} INFO  agent-controller - Successfully sent data")
            
            # Randomly show unusual traffic alert
            if random.random() < 0.3:  # 30% chance
                print(f"{current_time} WARN  agent-controller - Detected unusual network traffic on worker-02")
                print(f"{current_time} INFO  agent-controller - Alerting monitoring system")
            
            time.sleep(5)
            
            print("\n[{}] Press Ctrl+C to exit...".format(datetime.now().strftime("%H:%M:%S")))
            time.sleep(2)
            
        except KeyboardInterrupt:
            print("\nExiting K8s master simulation...")
            break

if __name__ == "__main__":
    simulate_k8s_master() 