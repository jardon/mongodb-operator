# Charmed MongoDB tutorial:
Ready to try out Charmed MongoDB? This tutorial will guide you through the steps to get Charmed MongoDB up and running. 

## Minimum requirements:
Before we start be sure you have the following requirements:
- Ubuntu 20.04(focal) or later.
- 8GB of RAM.
- 2 CPU threads.
- At least 20GB of available storage.
- Access to the internet for downloading the required snaps and charms.

## Install and prepare LXD:
The fastest, simplest way to get started with Charmed MongoDB is to set up a local LXD cloud. LXD is a system container and virtual machine manager; Charmed MongoDB will be run in one of these containers and managed by Juju. While this tutorial covers the basics of LXD, you can explore more LXD [here](https://linuxcontainers.org/lxd/getting-started-cli/). The first step on our journey is to install LXD. LXD is installed from a snap package:
```
sudo snap install lxd --classic
```

Next we need to run `lxd init` to perform post-installation tasks. For this tutorial the default parameters are preferred and the network bridge should be set to have no ipv6 addresses:
```
lxd init --auto
lxc network set lxdbr0 ipv6.address none 
```

In the next step we will install Juju. Juju speaks directly to the local LXD daemon, which also requires [lxd group membership](https://linuxcontainers.org/lxd/getting-started-cli/#access-control). Add `$USER` to the group lxd:
```
newgrp lxd
sudo adduser $USER lxd
```

You can list all LXD containers by entering the command `lxc list` in to the command line. Although at this point in the tutorial none should exist and you'll only see this as output:
```
+------+-------+------+------+------+-----------+
| NAME | STATE | IPV4 | IPV6 | TYPE | SNAPSHOTS |
+------+-------+------+------+------+-----------+
```

## Install and prepare Juju:
[Juju](https://juju.is/) is an operation Lifecycle manager(OLM) for clouds, bare metal, LXD or Kubernetes. We will be using it to deploy and manage Charmed MongoDB. As with LXD, Juju is installed from a snap package:
```
sudo snap install juju --classic
```

Juju already has a built-in knowledge of LXD and how it works, so there is no additional setup or configuration needed. A controller will be used to deploy and control Charmed MongoDB. All we need to do is run the command to bootstrap a Juju controller named ‘overlord’ to LXD. 
```
juju bootstrap localhost overlord
```

The Juju controller should exist within an LXD container. You can verify this by entering the command `lxc list` and you should see the following:
```
+---------------+---------+-----------------------+------+-----------+-----------+
|     NAME      |  STATE  |         IPV4          | IPV6 |   TYPE    | SNAPSHOTS |
+---------------+---------+-----------------------+------+-----------+-----------+
| juju-<id>     | RUNNING | 10.105.164.235 (eth0) |      | CONTAINER | 0         |
+---------------+---------+-----------------------+------+-----------+-----------+
```
where `<id>` is a unique combination of numbers and letters such as `9d7e4e-0`

The controller can work with different models; models host applications such as Charmed MongoDB. Set up a specific model for Charmed MongoDB named ‘tutorial’:
```
juju add-model tutorial
```

You can now view the model you created above by entering the command `juju status` into the command line. You should see the following:
```
Model    Controller  Cloud/Region         Version  SLA          Timestamp
tutorial overlord    localhost/localhost  2.9.37   unsupported  23:20:53Z

Model "admin/tutorial" is empty.
```

