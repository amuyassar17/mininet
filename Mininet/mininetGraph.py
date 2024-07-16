from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel

def spineLeafTopology():
    net = Mininet(controller=Controller, switch=OVSKernelSwitch, cleanup=True)

    # Membuat Controller
    c0 = net.addController('c0')

    # Membuat Spine Switches
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')

    # Membuat Leaf Switches
    leaf_switches = [net.addSwitch('s{}'.format(3+i)) for i in range(6)]

    # Membuat Hosts dan menghubungkannya ke leaf switches
    for i in range(6):
        for j in range(8):  # Sesuaikan jumlah host per switch jika perlu
            host = net.addHost('h{}'.format(i*8+j+1))
            net.addLink(host, leaf_switches[i])

    # Menghubungkan Leaf Switches ke Spine Switches
    for leaf in leaf_switches:
        net.addLink(leaf, s1)
        net.addLink(leaf, s2)

    return net

def save_topology(net):
    print("Saving topology to 'topology.graphml'")
    nodes = net.switches + net.hosts
    links = net.links

    graphml = ['<?xml version="1.0" encoding="UTF-8"?>']
    graphml.append('<graphml xmlns="http://graphml.graphdrawing.org/xmlns" '
                   'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                   'xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns '
                   'http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">')
    graphml.append('<graph id="G" edgedefault="directed">')

    for node in nodes:
        graphml.append(f'<node id="{node.name}"/>')

    for link in links:
        src = link.intf1.node.name
        dst = link.intf2.node.name
        graphml.append(f'<edge source="{src}" target="{dst}"/>')

    graphml.append('</graph>')
    graphml.append('</graphml>')

    with open('topology.graphml', 'w') as f:
        f.write('\n'.join(graphml))

    print("Topology saved to 'topology.graphml'")

if __name__ == '__main__':
    setLogLevel('info')
    myNetwork = spineLeafTopology()
    myNetwork.start()
    save_topology(myNetwork)
    CLI(myNetwork)
    myNetwork.stop()

