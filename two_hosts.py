from mininet.node import CPULimitedHost
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.link import TCIntf

class Topology(Topo):

    def build(self):
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')

        self.addLink(h1, h2, intf=TCIntf,
                     params1={'delay': '50ms', 'bw': 10, 'ip': '10.0.0.1/24'},
                     params2={'ip': '10.0.0.2/24'})
        self.addLink(h1, h2, intf=TCIntf,
                     params1={'delay': '50ms', 'bw': 10, 'ip': '10.1.0.1/24'},
                     params2={'ip': '10.1.0.2/24'})
        self.addLink(h1, h2, intf=TCIntf,
                     params1={'delay': '50ms', 'bw': 10, 'ip': '10.2.0.1/24'},
                     params2={'ip': '10.2.0.2/24'})


def run():
    topo = Topology()

    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    # net.setDefault('terminal', 'gnome-terminal')
    net.start()
    # FullNM(net)
    net.interact()


if __name__ == "__main__":
    setLogLevel("info")
    run()
