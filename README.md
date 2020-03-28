# netsec final

## Locations
kube-apiserver audit policy: `/etc/kubernetes/audit-policy.yaml` \
kube-apiserver audit log: `/etc/kubernetes/log/audit.log`

## Setup Instructions
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