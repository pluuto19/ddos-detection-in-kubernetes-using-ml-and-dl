#!/bin/bash
systemctl stop kubelet
rm -rf /etc/apt/keyrings/ /etc/apt/source.list.d/kubernetes.list /etc/apt/source.list.d/docker.list /etc/kubernetes/ /var/lib/kubelet/ /var/lib/etcd/ /var/log/containers/ /var/log/pods/ /etc/cni/net.d/ /opt/cni/bin
kill $(lsof -t -i:6443)