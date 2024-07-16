# File: mytopo.py

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController

class MyTopo(Topo):
    def build(self):
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        self.addLink(h1, s1)
        self.addLink(h2, s2)
        self.addLink(s1, s2)

if __name__ == '__main__':
    topo = MyTopo()
    net = Mininet(topo=topo, controller=RemoteController)
    net.start()
    net.pingAll()
    net.stop()

