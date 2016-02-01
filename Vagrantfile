# Installs a VM for developing manufactorum

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty32"

  config.vm.network "forwarded_port", guest: 5000, host: 5000

  # Install Python 3.4, redis and the required modules
  config.vm.provision "shell", inline: <<-SHELL
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip redis-server
    pip3 install --upgrade pip  # uses the ubuntu version of pip to install the latest pip as the pip command
    pip install -r /vagrant/requirements.txt
    echo "alias python=python3" >> ~/.bashrc  # make python3 the quasi-default for the vagrant user
  SHELL
end

# vi: set ft=ruby :
