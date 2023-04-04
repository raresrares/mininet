from mininet.node import CPULimitedHost
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.log import setLogLevel


class Topology(Topo):

    def build(self):
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')

        s1 = self.addSwitch('s1')

        self.addLink(h1, s1, cls=TCLink, delay='40ms', bw=8)
        self.addLink(h2, s1, cls=TCLink, delay='40ms', bw=8)
        self.addLink(h1, s1, cls=TCLink, delay='40ms', bw=8)
        self.addLink(h2, s1, cls=TCLink, delay='40ms', bw=8)


def run():
    topo = Topology()

    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)

    net.start()
    net.pingAll()
    net.interact()


if __name__ == "__main__":
    setLogLevel("info")
    run()
