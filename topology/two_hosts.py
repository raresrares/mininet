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
                     params1={'ip': '10.0.0.1/24'}, bw=8,
                     params2={'ip': '10.0.0.2/24'})
        self.addLink(h1, h2, intf=TCIntf,
                     params1={'ip': '10.1.0.1/24'}, bw=8,
                     params2={'ip': '10.1.0.2/24'})
        self.addLink(h1, h2, intf=TCIntf,
                     params1={'ip': '10.2.0.1/24'}, bw=8,
                     params2={'ip': '10.2.0.2/24'})

        h1.execCmd('ip mptcp endpoint flush')
        h1.execCmd('ip mptcp limits set subflow 2 add_addr_accepted 2')

        h1.execCmd('ip mptcp endpoint add 10.0.0.1 dev h1-eth0 id 1 subflow')
        h1.execCmd('ip mptcp endpoint add 10.1.0.1 dev h1-eth1 id 2 subflow')
        h1.execCmd('ip mptcp endpoint add 10.2.0.1 dev h1-eth2 id 3 subflow')

        h2.execCmd('ip mptcp endpoint flush')
        h2.execCmd('ip mptcp limits set subflow 2 add_addr_accepted 2')

        h2.execCmd('ip mptcp endpoint add 10.0.0.2 dev h2-eth0 id 1 subflow')
        h2.execCmd('ip mptcp endpoint add 10.1.0.2 dev h2-eth1 id 2 subflow')
        h2.execCmd('ip mptcp endpoint add 10.2.0.1 dev h2-eth2 id 3 subflow')


def run():
    topo = Topology()

    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()
    net.interact()


if __name__ == "__main__":
    setLogLevel("info")
    run()
