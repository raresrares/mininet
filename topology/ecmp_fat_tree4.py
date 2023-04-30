#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSSwitch, Host, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink


class BGPTopo(Topo):
    def build(self):
        # Add routers
        r1 = self.addSwitch('r1', cls=OVSSwitch, failMode='standalone')
        r2 = self.addSwitch('r2', cls=OVSSwitch, failMode='standalone')

        # Add hosts
        h1 = self.addHost('h1', ip='192.168.1.2/24',
                          defaultRoute='via 192.168.1.1')
        h2 = self.addHost('h2', ip='192.168.2.2/24',
                          defaultRoute='via 192.168.2.1')

        # Add links
        self.addLink(h1, r1)
        self.addLink(h2, r2)
        self.addLink(r1, r2, cls=TCLink, bw=10)


if __name__ == '__main__':
    setLogLevel('info')

    topo = BGPTopo()
    net = Mininet(topo=topo, controller=None)

    # Start the network
    net.start()

    # Configure FRR on routers
    net.get('r1').cmd('sysctl net.ipv4.ip_forward=1')
    net.get('r2').cmd('sysctl net.ipv4.ip_forward=1')
    net.get('r1').cmd('ip addr add 192.168.1.1/24 dev r1-eth0')
    net.get('r1').cmd('ip addr add 10.0.0.1/30 dev r1-eth1')
    net.get('r2').cmd('ip addr add 192.168.2.1/24 dev r2-eth0')
    net.get('r2').cmd('ip addr add 10.0.0.2/30 dev r2-eth1')

    # Start FRR daemons with the configuration files
    net.get('r1').cmd('frr -d -f r1.frr')
    net.get('r2').cmd('frr -d -f r2.frr')
    # Enter the CLI
    CLI(net)

    # Stop the network
    net.stop()

