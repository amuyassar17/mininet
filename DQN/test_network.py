# File: test_network.py

from mytopo import MyTopo
from mininet.net import Mininet
from mininet.node import RemoteController
import time
import os

def test_latency(net):
    h1 = net.get('h1')
    h2 = net.get('h2')
    result = h1.cmd('ping -c 10 %s' % h2.IP())
    latency = parse_ping_result(result)
    return latency

def test_throughput(net):
    h1 = net.get('h1')
    h2 = net.get('h2')
    h1.cmd('iperf -s &')
    result = h2.cmd('iperf -c %s' % h1.IP())
    throughput = parse_iperf_result(result)
    return throughput

def test_bandwidth(net):
    # Implementasikan pengujian bandwidth sesuai kebutuhan
    pass

def parse_ping_result(result):
    # Parsing hasil ping untuk mendapatkan latency rata-rata
    lines = result.split('\n')
    for line in lines:
        if 'avg' in line:
            latency = line.split('/')[4]
            return float(latency)
    return 0

def parse_iperf_result(result):
    # Parsing hasil iperf untuk mendapatkan throughput
    lines = result.split('\n')
    for line in lines:
        if 'Mbits/sec' in line:
            throughput = line.split(' ')[-2]
            return float(throughput)
    return 0

if __name__ == '__main__':
    os.system('sudo mn -c')
    topo = MyTopo()
    net = Mininet(topo=topo, controller=RemoteController)
    net.start()

    latency_before = test_latency(net)
    throughput_before = test_throughput(net)
    bandwidth_before = test_bandwidth(net)

    # Run network with DRL
    os.system('ryu-manager dqn_switch.py &')
    time.sleep(60)  # Wait for the controller to start

    latency_after = test_latency(net)
    throughput_after = test_throughput(net)
    bandwidth_after = test_bandwidth(net)

    net.stop()

    with open('network_metrics.csv', 'w') as f:
        f.write('Metric,Before,After\n')
        f.write(f'Latency,{latency_before},{latency_after}\n')
        f.write(f'Throughput,{throughput_before},{throughput_after}\n')
        f.write(f'Bandwidth,{bandwidth_before},{bandwidth_after}\n')

