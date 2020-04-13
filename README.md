# netsec final

## Locations
kube-apiserver audit policy: `/etc/kubernetes/audit-policy.yaml` \
kube-apiserver audit log: `/etc/kubernetes/log/audit.log`

## Setup Instructions
Expose security groups inbound rules:
 - Custom TCP Traffic, Port 22, Allow Anywhere
 - Custom TCP Traffic, Port 6443, Allow Anywhere
 - Custom TCP Traffic, Port 8080, Allow Anywhere
 - Custom TCP Traffic, Port 2379, Allow Anywhere
 - Custom TCP Traffic, Port 2380, Allow Anywhere
 - Custom TCP Traffic, Port 80, Allow Anywhere

SSH:
```bash
$ ssh ubuntu@$SERVER_IP -i $PRIV_KEY
```

Root:
```bash
$ sudo su
```

Install:
```bash
$ ./init_setup
```

Verify:
```bash
$ kubectl version --client
$ kubelet --version
$ kubeadm version
```

Start:
```bash
$ kubeadm init --ignore-preflight-errors=NumCPU --v=5 --config config_kubeadm.yaml
```

Ubuntu:
```bash
$ exit
```

Link:
```bash
$ mkdir -p $HOME/.kube
$ sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
$ sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

## Next

Record:
```bash
$ kubectl cluster-info
```

## Data Analysis

(1) Filter out uninteresting logs:
```bash
$ python3 parse_kube.py
$ python3 parse_etcd.py
```

(2) [Optional] Condense multiple `.json` results into one file:
```bash
$ python3 condense_kube.py
```

(3) Extract IPs from kube and etcd logs, then query for location (also populates `visual.html`):
```bash
$ python3 process_ips.py
$ python3 query_ipstack.py
```

(4) Interpret request URIs and time frequencies:
```bash
$ python3 process_request_uri.py
$ python3 process_time_freq.py
```

See webcrawlers.txt for some research into the web crawlers we saw activity from.
