#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel

def myNetwork():
    net = Mininet(controller=RemoteController, link=TCLink, switch=OVSKernelSwitch)
    
    # Add Controller
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)
    
    # Add Switches
    switches = []
    for i in range(5):
        switches.append(net.addSwitch(f's{i+1}'))
    
    # Add Hosts
    hosts = []
    for i in range(25):
        hosts.append(net.addHost(f'h{i+1}', ip=f'10.0.0.{i+1}'))
    
    # Add links between hosts and switches
    for i, host in enumerate(hosts):
        net.addLink(host, switches[i % 5])
    
    # Add links between switches to form a topology
    for i in range(5):
        net.addLink(switches[i], switches[(i + 1) % 5])
    
    net.build()
    c0.start()
    
    for switch in switches:
        switch.start([c0])
    
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()

