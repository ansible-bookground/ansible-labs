# Building AWX test environment on VirtualBox using Vagrant

## Example Network Topology:
```
-----------+----------- <NAT network>
           |
           |
     [eth0]|
    Virtual Machine
           |[eth1]
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
```

## Login the virtual machine and start minikube:
```shell
$ vagrant ssh
[vagrant@awx ~]$ minikube start --cpus='3' --memory='6g'
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
$ sudo route add -net 192.168.49.0/24 gw 192.168.57.4
```

Then, you can login the dashboard via http://192.168.49.2:30834 as `admin` user.

## Backup and Restore

Create persistent volume claim(awxbackup-pvc) to store backup contents:
```shell
$ cd work/awx/backup_restore/
$ kubectl apply -f pv.yaml
$ kubectl get pvc -n awx
NAME                                STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
awxbackup-pvc                       Bound    pvc-3124f0bb-0607-47da-9d63-9b0e000ae671   4Gi        RWO            standard       12m
postgres-13-awx-app-postgres-13-0   Bound    pvc-999653f8-c967-4f4d-b43e-341693ea2064   8Gi        RWO            standard       20m
$ kubectl describe pvc/awxbackup-pvc -n awx
Name:          awxbackup-pvc
Namespace:     awx
StorageClass:  standard
Status:        Bound
Volume:        pvc-3124f0bb-0607-47da-9d63-9b0e000ae671
Labels:        <none>
Annotations:   pv.kubernetes.io/bind-completed: yes
               pv.kubernetes.io/bound-by-controller: yes
               volume.beta.kubernetes.io/storage-provisioner: k8s.io/minikube-hostpath
               volume.kubernetes.io/storage-provisioner: k8s.io/minikube-hostpath
Finalizers:    [kubernetes.io/pvc-protection]
Capacity:      4Gi
Access Modes:  RWO
VolumeMode:    Filesystem
Used By:       <none>
Events:
  Type    Reason                 Age                From                                                                    Message
  ----    ------                 ----               ----                                                                    -------
  Normal  ExternalProvisioning   13m (x2 over 13m)  persistentvolume-controller                                             Waiting for a volume to be created either by the external provisioner 'k8s.io/minikube-hostpath' or manually by the system administrator. If volume creation is delayed, please verify that the provisioner is running and correctly registered.
  Normal  Provisioning           13m                k8s.io/minikube-hostpath_minikube_33ff3578-90c5-486c-971b-e7ced9aabbe4  External provisioner is provisioning volume for claim "awx/awxbackup-pvc"
  Normal  ProvisioningSucceeded  13m                k8s.io/minikube-hostpath_minikube_33ff3578-90c5-486c-971b-e7ced9aabbe4  Successfully provisioned volume pvc-3124f0bb-0607-47da-9d63-9b0e000ae671
```

Generate backup and restore manifest files:
```shell
$ ./generate_manifest.sh
$ ./generate_manifest.sh
Backup manifest:./manifest/fc10496e-f6b5-4802-85b7-a94c134d3b27/backup.yaml has been created.
Restore manifest:./manifest/fc10496e-f6b5-4802-85b7-a94c134d3b27/restore.yaml has been created
```

Backup AWX system:
```shell
$ kubectl apply -f ./manifest/fc10496e-f6b5-4802-85b7-a94c134d3b27/backup.yaml
$ kubectl logs deployments/awx-operator-controller-manager -f -n awx
```

Restore AWX system:
```shell
$ kubectl apply -f ./manifest/fc10496e-f6b5-4802-85b7-a94c134d3b27/restore.yaml
$ kubectl logs deployments/awx-operator-controller-manager -f -n awx
```
