from mininet.net import Mininet
from mininet.node import Host
from mininet.topo import Topo
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info
from subprocess import call


class LinuxRouter(Host):
    "A Node with IP forwarding enabled."

    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()


class NetworkTopo(Topo):
    "BGP network topology."

    def build(self, **_opts):

        defaultIP = '192.168.1.1/24'
        router = self.addNode('r0', cls=LinuxRouter, ip=defaultIP)

        h1 = self.addHost('h1',
                          ip='192.168.1.100/24',
                          defaultRoute='via 192.168.1.1')
        h2 = self.addHost('h2',
                          ip='172.16.0.100/24',
                          defaultRoute='via 172.16.0.1')
        h3 = self.addHost('h3',
                          ip='10.0.0.100/24',
                          defaultRoute='via 10.0.0.1')

        self.addLink(h1, router,
                     intfName2='r0-eth1',
                     params2={'ip': '192.168.1.1/24'})
        self.addLink(h2, router,
                     intfName2='r0-eth2',
                     params2={'ip': '172.16.0.1/24'})
        self.addLink(h3, router,
                     intfName2='r0-eth3',
                     params2={'ip': '10.0.0.1/24'})


def run():
    "Test BGP network topology"
    topo = NetworkTopo()
    net = Mininet(topo=topo)
    net.start()

    info('*** Routing Table on Router:\n')
    print(net['r0'].cmd('route'))

    net.pingAll()
    net.interact()
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()
