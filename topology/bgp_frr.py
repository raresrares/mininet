from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink

class LinuxRouter(Node):
    "A Node with IP forwarding enabled."

    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()


class NetworkTopo(Topo):
    def build(self):
        defaultIP = '10.0.1.1/24'
        router1 = self.addNode('r0', cls=LinuxRouter, ip=defaultIP)

        defaultIP = '10.0.2.1/24'
        router2 = self.addNode('r1', cls=LinuxRouter, ip=defaultIP)

        defaultIP = '10.0.3.1/24'
        router3 = self.addNode('r2', cls=LinuxRouter, ip=defaultIP)

        h1 = self.addHost('h1', ip='10.0.1.100/24',
                          defaultRoute='via 10.0.1.1',
                          bw=8, delay='10ms', loss=0)
        h2 = self.addHost('h2', ip='10.0.2.100/24',
                          defaultRoute='via 10.0.2.1',
                          bw=8, delay='10ms', loss=0)
        h3 = self.addHost('h3', ip='10.0.3.100/24',
                          defaultRoute='via 10.0.3.1',
                          bw=8, delay='10ms', loss=0)

        self.addLink(h1, router1,
                     intfName2='r0-eth1',
                     params2={'ip': '10.0.1.1/24'},
                     bw=8, delay='10ms', loss=0)
        self.addLink(h2, router2,
                     intfName2='r1-eth1',
                     params2={'ip': '10.0.2.1/24'},
                     bw=8, delay='10ms', loss=0)
        self.addLink(h3, router3,
                     intfName2='r2-eth1',
                     params2={'ip': '10.0.3.1/24'},
                     bw=8, delay='10ms', loss=0)

        self.addLink(router1,
                     router2,
                     intfName1='r0-eth2',
                     intfName2='r1-eth2',
                     params1={'ip': '10.0.12.1/24'},
                     params2={'ip': '10.0.12.2/24'},
                     bw=8, delay='10ms', loss=0)
        self.addLink(router2,
                     router3,
                     intfName1='r1-eth3',
                     intfName2='r2-eth2',
                     params1={'ip': '10.0.23.1/24'},
                     params2={'ip': '10.0.23.2/24'},
                     bw=8, delay='10ms', loss=0)
        self.addLink(router3,
                     router1,
                     intfName1='r2-eth3',
                     intfName2='r0-eth3',
                     params1={'ip': '10.0.31.1/24'},
                     params2={'ip': '10.0.31.2/24'},
                     bw=8, delay='10ms', loss=0)


def run():
    "Test linux router"
    topo = NetworkTopo()
    net = Mininet(topo=topo, controller=None, link=TCLink)
    net.start()

    info('*** Routing Table on Router:\n')
    for router in ['r0', 'r1', 'r2']:
        info(net[router].cmd('route'))

    router1, router2, router3 = net.getNodeByName('r0', 'r1', 'r2')

    router1.cmd('ip route add 10.0.2.0/24 via 10.0.12.2')
    router1.cmd('ip route add 10.0.3.0/24 via 10.0.31.1')

    router2.cmd('ip route add 10.0.1.0/24 via 10.0.12.1')
    router2.cmd('ip route add 10.0.3.0/24 via 10.0.23.2')

    router3.cmd('ip route add 10.0.1.0/24 via 10.0.31.2')
    router3.cmd('ip route add 10.0.2.0/24 via 10.0.23.1')

    info('*** Routing Table on Router after adding static route:\n')
    for router in ['r0', 'r1', 'r2']:
        info(net[router].cmd('route'))

    info('*** Running CLI\n')
    net.pingAll()
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()

