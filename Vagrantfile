$script = <<SCRIPT

# Exit immediately if a command exits with a non-zero status.
set -e

sudo apt-get update
sudo apt-get install -y python3-pip

cd /vagrant
sudo pip3 install -r requirements.txt

SCRIPT



Vagrant.configure("2") do |config|
  config.vm.box = 'debian/buster64'
  config.vm.provision 'shell', inline: $script, privileged: false
end
