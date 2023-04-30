#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import OVSSwitch, Controller, RemoteController
from mininet.cli import CLI


class FatTreeTopo(Topo):
    def build(self):
        routers = []
        hosts = []

        for i in range(1, 10):
            host = self.addHost(f'h{i}')
            hosts.append(host)

        for i in range(1, 6):
            router = self.addSwitch(f's{i}')
            routers.append(router)

        router_1 = self.addSwitch('s1')
        router_2 = self.addSwitch('s2')
        router_3 = self.addSwitch('s3')
        router_4 = self.addSwitch('s4')
        router_5 = self.addSwitch('s5')

        self.addLink(router_1, router_4)
        self.addLink(router_1, router_5)
        self.addLink(router_2, router_4)
        self.addLink(router_2, router_5)
        self.addLink(router_3, router_4)
        self.addLink(router_3, router_5)

        for i in range(1, 10):
            host = self.addHost(f'h{i}')
            if i <= 3:
                self.addLink(host, router_1)
            elif i <= 6:
                self.addLink(host, router_2)
            else:
                self.addLink(host, router_3)


def simpleTest():
    topo = FatTreeTopo()
    net = Mininet(topo=topo, switch=OVSSwitch,
                  controller=RemoteController, autoSetMacs=True, autoStaticArp=True)
    net.start()

    net.pingAll()

    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    simpleTest()
