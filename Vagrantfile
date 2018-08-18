# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  # config.vm.box = "hashicorp/precise64"

  # for box LXC
  # config.vm.box = "fgrehm/trusty64-lxc"

  # for VB
  config.vm.box = "ubuntu/trusty64"

  config.vm.network "forwarded_port", guest: 80, host: 8480
  config.vm.network "forwarded_port", guest: 4200, host: 4200
  
  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # NOTE: This will enable public access to the opened port
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine and only allow access
  # via 127.0.0.1 to disable public access
  # config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  # config.vm.provision "shell", inline: <<-SHELL
  #   apt-get update
  #   apt-get install -y apache2
  # SHELL

  # provisioning
  config.vm.provision "shell", inline: <<-SHELL
    # something that set locales
    sudo locale-gen uk_UA.UTF-8 uk_UA uk_UA.UTF-8
    sudo dpkg-reconfigure locales

    sudo apt-get update

    # installing nginx
    sudo apt-get install -y nginx

    # installing pip/setuptools/wheel
    sudo apt-get install -y python-pip python-dev

    # install virtualenv
    sudo pip install virtualenv

    # activate virtual enviroment
    virtualenv /vagrant/backend/app_venv
    source /vagrant/backend/app_venv/bin/activate

    sudo /vagrant/backend/app_venv/bin/pip install uwsgi flask Flask-Mail simplejson psycopg2-binary validate_email pyDNS

    # config nginx by copy config
    sudo cp /vagrant/backend/config/nginx_config.conf /etc/nginx/sites-available/matcha
    sudo ln -s /etc/nginx/sites-available/matcha /etc/nginx/sites-enabled
    sudo rm /etc/nginx/sites-enabled/default

    # then restart nginx
    sudo service nginx stop
    sudo service nginx start

    # run uwsgi
    sudo cp /vagrant/backend/config/matcha_config.conf /etc/init/matcha.conf
    sudo start matcha

    # install psql
    sudo apt-get install postgresql postgresql-contrib

    # if locales was not set on beginning - the cluster would not be created and psql not started, so:
    # sudo locale-gen uk_UA.UTF-8 uk_UA uk_UA.UTF-8
    # sudo dpkg-reconfigure locales
    # sudo pg_createcluster 9.3 main --start
    # sudo service postgresql start

    # change deploy folder owners
    sudo chown vagrant:www-data -R /vagrant/

    # install nodejs npm
    # curl -sL https://deb.nodesource.com/setup_9.x | sudo -E bash -
    # sudo apt-get install -y nodejs
    # sudo npm install --unsafe-perm -g @angular/cli


  SHELL

end