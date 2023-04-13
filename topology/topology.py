from mininet.node import CPULimitedHost
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.log import setLogLevel

import info


class Topology(Topo):
    def build(self, nr=2, nh=2):
        routers = []
        # Add routers to topology
        for i in range(nr):
            routers.append(self.addHost(info.get("router_name", i)))

        # Add links between routers
        for i in range(nr):
            for j in range(i + 1, nr):
                ifn1 = info.get("r2r_if_name", i, j)
                ifn2 = info.get("r2r_if_name", j, i)
                self.addLink(routers[i], routers[j],
                             intfName1=ifn1, intfName2=ifn2)
        # Add links between routes and hosts
        for i in range(nr):
            host = self.addHost(info.get("host_name", i))
            i1 = info.get("host_if_name", i)
            for j in range(nh):
                if i == j:
                    i2 = info.get("router_if_name", j)
                    self.addLink(host, routers[i], intfName1=i1, intfName2=i2)


class FullNM(object):
    def __init__(self, net, n_routers, n_hosts):
        self.net = net
        self.hosts = []
        self.routers = []
        self.n_hosts = n_hosts

        for i in range(n_hosts):
            r = self.net.get(info.get("router_name", i))
            hosts = []

            for j in range(n_hosts):
                hidx = i * n_hosts + j
                h = self.net.get(info.get("host_name", hidx))
                hosts.append(h)
                self.hosts.append(h)

            self.routers.append((r, hosts))


def run():
    topo = Topology()

    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)

    net.start()
    net.interact()


if __name__ == "__main__":
    setLogLevel("info")
    run()
