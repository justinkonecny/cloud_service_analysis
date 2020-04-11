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

See webcrawler.docx for some research into the web crawlers we saw activity from.
