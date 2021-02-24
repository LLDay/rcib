Vagrant.configure("2") do |config|

  config.vm.define "ubuntu" do |ubuntu|
    ubuntu.vm.box = "ubuntu/xenial64"
    ubuntu.vm.network "public_network", ip: "192.168.0.30", bridge: 'wlo1'
    ubuntu.vm.provider :virtualbox do |vb|
        vb.name = "ubuntu"
        vb.memory = 512
        vb.cpus = 1
    end
    ubuntu.vm.provision "shell", path: "scripts/bash/prepare_environment.sh", args: '/vagrant'
  end

  config.vm.define "windows" do |windows|
    windows.vm.box = "gusztavvargadr/windows-server"
    windows.vm.network "public_network", ip: "192.168.0.31", bridge: 'wlo1'
    windows.vm.provider :virtualbox do |vb|
        vb.name = "windows"
        vb.memory = 1536
        vb.cpus = 1
    end
    windows.vm.provision "shell", path: "scripts/powershell/prepare_environment.ps1"
  end

end
