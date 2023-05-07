# Test VM

This virtual machine is used for testing of Jupyter server. The server is actually deployed on a
real machine.

## Introduction

For the VM, we used Vagrant so it's easier to provision the machine to the spec we need. Box used
for the VM is `generic/rocky9` which is a very basic Rocky Linux 9 box. The ip is hardcoded so it
would be easier to test with Ansible.

VM is provisioned with a root ssh key so we can connect directly as root and execute all playbooks
(they are very superuser intensive so it's easier to just use root).

After provisioning we can access the root user through the hardcoded ip and provided key. This key
should not be used for production!

## Usage

To run the VM, just start it as a regular Vagrant machine:

```sh
$ vagrant up
```
