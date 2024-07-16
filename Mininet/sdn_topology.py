from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def customTopology():
    "Create a network with 8 switches and 100 hosts."

    net = Mininet(controller=RemoteController, switch=OVSSwitch)

    # Tambahkan controller Ryu
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)

    # Tambahkan switch
    switches = [net.addSwitch('s%d' % i) for i in range(1, 9)]

    # Tambahkan host dan menghubungkannya ke switch
    for i in range(100):
        host = net.addHost('h%d' % (i + 1))
        net.addLink(host, switches[i % 8])

    # Menghubungkan switch satu sama lain untuk membentuk pohon
    net.addLink(switches[0], switches[1])
    net.addLink(switches[0], switches[2])
    net.addLink(switches[1], switches[3])
    net.addLink(switches[1], switches[4])
    net.addLink(switches[2], switches[5])
    net.addLink(switches[2], switches[6])
    net.addLink(switches[3], switches[7])

    # Start jaringan
    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    customTopology()
