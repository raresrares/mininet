from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.log import setLogLevel


class NetworkTopo(Topo):
    def build(self):
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')

        # add three links between h1 and h2
        for _ in range(3):
            self.addLink(h1, h2)


def run():
    topo = NetworkTopo()

    net = Mininet(topo=topo)

    net.start()
    net.pingAll()
    net.interact()


if __name__ == "__main__":
    setLogLevel("info")
    run()
