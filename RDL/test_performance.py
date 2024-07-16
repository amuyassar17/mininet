from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.link import TCLink
from mininet.log import setLogLevel

def testNetworkPerformance():
    net = Mininet(controller=RemoteController, link=TCLink)
    net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)
    
    # Define the same topology as before
    switches = []
    for i in range(5):
        switches.append(net.addSwitch(f's{i+1}'))
    
    hosts = []
    for i in range(25):
        hosts.append(net.addHost(f'h{i+1}', ip=f'10.0.0.{i+1}'))
    
    for i, host in enumerate(hosts):
        net.addLink(host, switches[i % 5])
    
    for i in range(5):
        net.addLink(switches[i], switches[(i + 1) % 5])
    
    net.build()
    net.start()
    
    # Testing Latency
    print("Testing Latency between h1 and h2")
    h1, h2 = net.get('h1', 'h2')
    net.ping([h1, h2])
    
    # Testing Bandwidth
    print("Testing Bandwidth between h1 and h2")
    h1, h2 = net.get('h1', 'h2')
    h2.cmd('iperf -s &')
    h1.cmd('iperf -c 10.0.0.2')
    
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    testNetworkPerformance()

