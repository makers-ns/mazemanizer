# Create .ssh directory
mkdir -p /root/.ssh
chmod 700 /root/.ssh

# Install authorized_keys
cp /home/vagrant/key.pub /root/.ssh/authorized_keys

# Set permissions
chmod 600 /root/.ssh/authorized_keys

# Remove key.pub
rm /home/vagrant/key.pub
