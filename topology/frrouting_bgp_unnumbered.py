
#!/usr/bin/env python

from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI
import time

frr_conf = '''
frr defaults datacenter
!
hostname {name}
password zebra
!
router bgp {asnum}
 bgp router-id  {router_id}
 bgp bestpath as-path multipath-relax
 no bgp network import-check
 neighbor {neighbor_ip} remote-as {remote_as}
 address-family ipv4 unicast
  network {router_id}/32
  network {network}
 exit-address-family
!
line vty
!
end
'''

vtysh_conf = '''
service integrated-vtysh-config
'''

daemons = '''
bgpd=yes
vtysh_enable=yes
zebra_options="  -A 127.0.0.1 -s 90000000"
bgpd_options="   -A 127.0.0.1"
'''


def put_file(host, file_name, content, **kwargs):
    with open("/tmp/tmp", mode="w") as f:
        f.write(content.format(**kwargs))
    host.cmdPrint("cp /tmp/tmp " + file_name)


def run():
    setLogLevel('info')
    net = Mininet()

    privateDirs = ['/etc/frr', '/var/run/frr']
    h1 = net.addHost('h1', ip='192.168.0.1/24',
                     privateDirs=privateDirs, asnum=65001)
    h2 = net.addHost('h2', ip='192.168.0.2/24',
                     privateDirs=privateDirs, asnum=65002)

    net.addLink(h1, h2,
                intfName1='h1-eth0',
                intfName2='h2-eth0',
                bw=8, delay='5ms', loss=0)

    net.start()

    for i, h in enumerate(net.hosts):
        neighbor_ip = net.hosts[1].IP()\
            if h.name == 'h1' else net.hosts[0].IP()
        remote_as = net.hosts[1].params['asnum']\
            if h.name == 'h1' else net.hosts[0].params['asnum']

        put_file(h, "/etc/frr/daemons", daemons)
        put_file(h, "/etc/frr/vtysh.conf", vtysh_conf)
        put_file(h, "/etc/frr/frr.conf",
                 frr_conf,
                 name=h.name,
                 router_id=h.IP(),
                 asnum=h.params['asnum'],
                 network='192.168.0.{}/32'.format(i+1),
                 neighbor_ip=neighbor_ip,
                 remote_as=remote_as)

        h.cmd("/usr/lib/frr/frrinit.sh start")
        # h.cmd('ip address add 192.168.1.{}/32 dev {}-eth0'.format(i+1, h.name))

    time.sleep(5)

    h1.cmdPrint('vtysh -c "show bgp summary"')
    h1.cmdPrint('vtysh -c "show ip bgp"')
    h1.cmdPrint('ip route')

    h2.cmdPrint('vtysh -c "show bgp summary"')
    h2.cmdPrint('vtysh -c "show ip bgp"')
    h2.cmdPrint('ip route')

    # send ping in the advertised route
    h1.cmdPrint('ping -c 1 192.168.0.2')
    h2.cmdPrint('ping -c 1 192.168.0.1')
    CLI(net)
    net.stop()
    return 0


if __name__ == '__main__':
    run()
