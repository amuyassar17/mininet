import matplotlib.pyplot as plt
import numpy as np

def plot_performance(bandwidth_before, bandwidth_after, latency_before, latency_after):
    labels = ['Before DRL', 'After DRL']
    bandwidth = [bandwidth_before, bandwidth_after]
    latency = [latency_before, latency_after]
    
    x = np.arange(len(labels))
    width = 0.35
    
    fig, ax1 = plt.subplots()

    ax1.bar(x - width/2, bandwidth, width, label='Bandwidth')
    ax1.set_xlabel('Condition')
    ax1.set_ylabel('Bandwidth (Mbps)')
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels)
    
    ax2 = ax1.twinx()
    ax2.bar(x + width/2, latency, width, color='orange', label='Latency')
    ax2.set_ylabel('Latency (ms)')
    
    fig.tight_layout()
    plt.legend(loc='upper left')
    plt.show()

bandwidth_before = 50
bandwidth_after = 100
latency_before = 10
latency_after = 5

plot_performance(bandwidth_before, bandwidth_after, latency_before, latency_after)

