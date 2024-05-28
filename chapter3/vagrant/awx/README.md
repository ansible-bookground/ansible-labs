# Building AWX test environment on VirtualBox using Vagrant

## Example Network Topology:
```
-------+--------------- <NAT network>
       |
-------|-------+------- <public network(bridge):DHCP>
       |       |
       |       |
 [eth0]|       |[eth1]
    Virtual Machine
           |[eth2]
           |
           |.4
-----------+----------- <private network:192.168.57.0/24>
```

## Step to build environment

Checkout the `labs` repository:
```shell
$ git clone https://github.com/ansible-bookground/labs.git
$ cd lab
```

Install [vagrant-vbguest](https://github.com/dotless-de/vagrant-vbguest) plugin which automatically installs the host's VirtualBox Guest Additions on the guest system.

```shell
$ vagrant plugin install vagrant-vbguest
```

Install [vagrant-hostsupdater](https://github.com/agiledivider/vagrant-hostsupdater) plugin if you want to update `/etc/hosts` in the virtualbox host during the deployment process:
```shell
$ vagrant plugin install vagrant-hostsupdater
```

Vagrant up!:
```shell
$ vagrant up
==> awx: Available bridged network interfaces:
1) wlo1
2) enp3s0
...
==> awx: When choosing an interface, it is usually the one that is
==> awx: being used to connect to the internet.
==> awx:
    awx: Which interface should the network bridge to? 1  #<=Choose the numbwer of bridge network interface
```

## Login the virtual machine and start minikube:
```shell
$ vagrant ssh
[vagrant@awx ~]$ minikube start --cpus='2' --memory='4096m'
😄  minikube v1.32.0 on Redhat 9.3 (vbox/amd64)
✨  Automatically selected the podman driver. Other choices: ssh, none
📌  Using Podman driver with root privileges
👍  Starting control plane node minikube in cluster minikube
🚜  Pulling base image ...
💾  Downloading Kubernetes v1.28.3 preload ...
    > gcr.io/k8s-minikube/kicbase...:  453.90 MiB / 453.90 MiB  100.00% 9.45 Mi
    > preloaded-images-k8s-v18-v1...:  403.35 MiB / 403.35 MiB  100.00% 7.82 Mi
E0130 05:20:15.113290   11324 cache.go:189] Error downloading kic artifacts:  not yet implemented, see issue #8426
🔥  Creating podman container (CPUs=2, Memory=4096MB) ...
🐳  Preparing Kubernetes v1.28.3 on Docker 24.0.7 ...
    ▪ Generating certificates and keys ...
    ▪ Booting up control plane ...
    ▪ Configuring RBAC rules ...
🔗  Configuring bridge CNI (Container Networking Interface) ...
🔎  Verifying Kubernetes components...
    ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
🌟  Enabled addons: default-storageclass, storage-provisioner
🏄  Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default
[vagrant@awx ~]$
```

## Deploy AWX using minikube

Stage1: Deopy awx-operator.

```shell
[vagrant@awx ~]$ kubectl apply -k work/awx/stage1/
namespace/awx created
customresourcedefinition.apiextensions.k8s.io/awxbackups.awx.ansible.com created
customresourcedefinition.apiextensions.k8s.io/awxrestores.awx.ansible.com created
customresourcedefinition.apiextensions.k8s.io/awxs.awx.ansible.com created
serviceaccount/awx-operator-controller-manager created
role.rbac.authorization.k8s.io/awx-operator-awx-manager-role created
role.rbac.authorization.k8s.io/awx-operator-leader-election-role created
clusterrole.rbac.authorization.k8s.io/awx-operator-metrics-reader created
clusterrole.rbac.authorization.k8s.io/awx-operator-proxy-role created
rolebinding.rbac.authorization.k8s.io/awx-operator-awx-manager-rolebinding created
rolebinding.rbac.authorization.k8s.io/awx-operator-leader-election-rolebinding created
clusterrolebinding.rbac.authorization.k8s.io/awx-operator-proxy-rolebinding created
configmap/awx-operator-awx-manager-config created
service/awx-operator-controller-manager-metrics-service created
deployment.apps/awx-operator-controller-manager created
[vagrant@awx ~]$
```

Stage2: Deploy AWX application.
```shell
[vagrant@awx ~]$ kubectl get pods -n awx
NAME                                               READY   STATUS    RESTARTS   AGE
awx-operator-controller-manager-775bd7b75d-s8hj4   2/2     Running   0          67s
[vagrant@awx ~]$ kubectl apply -k work/awx/stage2/
deployment.apps/awx-operator-controller-manager created
[vagrant@awx ~]$ kubectl get pods -n awx
NAME                                               READY   STATUS    RESTARTS   AGE
awx-operator-controller-manager-775bd7b75d-s8hj4   2/2     Running   0          67s
[vagrant@awx ~]$ kubectl apply -k work/awx/stage2/
namespace/awx unchanged
customresourcedefinition.apiextensions.k8s.io/awxbackups.awx.ansible.com unchanged
customresourcedefinition.apiextensions.k8s.io/awxrestores.awx.ansible.com unchanged
customresourcedefinition.apiextensions.k8s.io/awxs.awx.ansible.com unchanged
serviceaccount/awx-operator-controller-manager unchanged
role.rbac.authorization.k8s.io/awx-operator-awx-manager-role configured
role.rbac.authorization.k8s.io/awx-operator-leader-election-role unchanged
clusterrole.rbac.authorization.k8s.io/awx-operator-metrics-reader unchanged
clusterrole.rbac.authorization.k8s.io/awx-operator-proxy-role unchanged
rolebinding.rbac.authorization.k8s.io/awx-operator-awx-manager-rolebinding unchanged
rolebinding.rbac.authorization.k8s.io/awx-operator-leader-election-rolebinding unchanged
clusterrolebinding.rbac.authorization.k8s.io/awx-operator-proxy-rolebinding unchanged
configmap/awx-operator-awx-manager-config unchanged
service/awx-operator-controller-manager-metrics-service unchanged
deployment.apps/awx-operator-controller-manager unchanged
awx.awx.ansible.com/awx-app created
[vagrant@awx ~]$ kubectl get pods -n awx
NAME                                               READY   STATUS    RESTARTS   AGE
awx-app-postgres-13-0                              1/1     Running   0          2m12s
awx-app-task-98f94bd49-r5ngf                       4/4     Running   0          99s
awx-app-web-565f4dbc89-84bz4                       3/3     Running   0          8s
awx-operator-controller-manager-775bd7b75d-s8hj4   2/2     Running   0          3m57s
[vagrant@awx ~]$ kubectl get svc -n awx
NAME                                              TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
awx-app-postgres-13                               ClusterIP   None            <none>        5432/TCP       2m55s
awx-app-service                                   NodePort    10.102.21.232   <none>        80:30834/TCP   2m24s
awx-operator-controller-manager-metrics-service   ClusterIP   10.99.42.221    <none>        8443/TCP       4m40s
```

Confirm service URL using minikube command:
```shell
[vagrant@awx ~]$ minikube service awx-app-service -n awx --url
http://192.168.49.2:30834
```

Confirm the admin password of AWX:
```shell
$ kubectl get secret -n awx awx-app-admin-password -o jsonpath="{.data.password}" | base64 --decode ; echo
```

On the `virtualbox host that the virtualbox is running`, you need to add the following routing to access container node ports on minikube:
```shell
$ sudo route add -net 192.168.49.0/24 <Virtual Machine "eth1" IPaddress>
```

Then, you can login the dashboard via http://192.168.49.2:30834 as `admin` user.
