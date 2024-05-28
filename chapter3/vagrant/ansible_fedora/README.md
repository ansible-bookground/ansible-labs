# Building Ansible products test environment on VirtualBox using Vagrant

## Example Network Topology:
```
-----------+---------- <NAT network>
           |
           |
           |[eth0]
    Virtual Machine
           |[eth1]
           |
           |.3
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

Note: If you want to use virtualbox host directory that is mounted on bind mountpoint, you should use `vagrant ssh`.

## Confirm installed ansible products

```
$ ansible --version
ansible [core x.y.z]
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/home/ansible/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python3.9/site-packages/ansible
  ansible collection location = /home/ansible/.ansible/collections:/usr/share/ansible/collections
  executable location = /usr/bin/ansible
  python version = 3.9.18 (main, Sep  7 2023, 00:00:00) [GCC 11.4.1 20230605 (Red Hat 11.4.1-2)] (/usr/bin/python3)
  jinja version = 3.1.2
  libyaml = True

$ ansible-navigator --version
ansible-navigator x.y.z

$ ansible-builder --version
x.y.z
```
