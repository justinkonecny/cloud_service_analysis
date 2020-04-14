# Cloud Service Bruteforcing

## Locations
kube-apiserver audit policy: `/etc/kubernetes/audit-policy.yaml` \
kube-apiserver audit log: `/etc/kubernetes/log/audit.log`

## Setup Instructions
On AWS, expose the following **inbound** rules on the EC2's security group:
 - Custom TCP Traffic, Port 22, Allow Anywhere
 - Custom TCP Traffic, Port 6443, Allow Anywhere
 - Custom TCP Traffic, Port 2379, Allow Anywhere
 - Custom TCP Traffic, Port 2380, Allow Anywhere

(1) SSH into the EC2:
```bash
$ ssh ubuntu@$SERVER_IP -i $PRIV_KEY
```

(2) Switch to the user `root`:
```bash
$ sudo su
```

(3) Perform setup installation:
```bash
$ ./init_setup
```

(4) Verify that the setup was successful:
```bash
$ kubectl version --client
$ kubelet --version
$ kubeadm version
```

(5) Start kubernetes:
```bash
$ kubeadm init --ignore-preflight-errors=NumCPU --v=5 --config config_kubeadm.yaml
```

(6) Drop back to the user `ubuntu`:
```bash
$ exit
```

(7) Configure the current setup for `ubuntu`:
```bash
$ mkdir -p $HOME/.kube
$ sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
$ sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

## Interacting

To view cluster information:
```bash
$ kubectl cluster-info
```

## Data Analysis

(1) Filter out uninteresting logs from the `.log` files to produce a results `.json`:
```bash
$ python3 parse_kube.py
$ python3 parse_etcd.py
```

(2) [Optional] Condense multiple `.json` results into one file:
```bash
$ python3 condense_kube.py
```

(3) Extract the IPs from kubernetes and etcd logs, then query for geolocation (also populates `visual.html`):
```bash
$ python3 process_ips.py
$ python3 query_ipstack.py
```

(4) Interpret request URIs and time frequencies (only to stdout):
```bash
$ python3 process_request_uri.py
$ python3 process_time_freq.py
```

(5) View interactive map:
 - Add your Google GeoCharts API key to `mapApiKey` in `visual.html`
 - Ensure `visuals/combined_ip_coordinates.json` is properly populated with coordinates
 - Open `visual.html` in Google Chrome

\
See `webcrawlers.txt` for some research into the web crawlers we saw activity from.
