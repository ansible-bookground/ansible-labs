# Building RHEL9 managed nodes on VirtualBox using Vagrant

## Example Network Topology:
```
-----------+---------- <NAT network>
           |
           |
           |[eth0]
    node00.example.com
           |[eth1]
           |
           |.10
-----------+---------- <private network:192.168.57.0/24>

-----------+---------- <NAT network>
           |
           |
           |[eth0]
    node01.example.com
           |[eth1]
           |
           |.11
-----------+---------- <private network:192.168.57.0/24>

-----------+---------- <NAT network>
           |
           |
           |[eth0]
    node02.example.com
           |[eth1]
           |
           |.11
-----------+---------- <private network:192.168.57.0/24>
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

## Login the virtual machine:

You will be able to login `vagrant ssh` in the vagrant working directory. Or you can use `ssh <VBOX_USERNAME>@<IPADDRESS or HOSTNAME>` if you want.
