# Ansible playbook

We're using Ansible for easy setup of the server. All the tasks are very basic and noninteractive so
it's easy to use a tool like Ansible.

## setup_lab.yaml

This playbook runs `create_proxy` and `create_services` role which will do everything that's
neccessary for the server to work.

The docs for the roles could be found in their respective directories.

## Usage

To use a playbook, you would want tun it using the `asnible-playbook` command.

```sh
$ ansible-playbook -i inventory/<inventory file> setup_lab.yaml
```

The inventory file should be created for specific use case you need. The provided one is one used
for testing on a VM but for anything else, you should create a new one which will define hosts in a
`labs` group.

## Variables

The variables need to define the users based on which the Jupyter servers and reverse proxy are
created. They should be stored in the `users` array and should be an object of the following
structure.

```yaml
users:
  - name: username # needs to be different for each user
  - port: 2000 # publish port for the jupyer server, just needs to be different for each user
  - hash: # password hash for the user, it can be the same for each user
```
