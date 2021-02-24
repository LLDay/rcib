import vagrant

va = vagrant.Vagrant()
command = 'python3 /vagrant/scripts/python/run_tests.py'

for machine in va.status():
    if machine.state != 'poweroff':
        print(va.ssh(machine.name, command=command))
