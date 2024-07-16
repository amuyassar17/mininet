# File: plot_metrics.py

import matplotlib.pyplot as plt
import pandas as pd

def plot_metrics():
    data = pd.read_csv('network_metrics.csv')
    metrics = data['Metric']
    before = data['Before']
    after = data['After']

    x = range(len(metrics))

    fig, ax = plt.subplots()
    ax.bar(x, before, width=0.4, label='Before DRL', align='center')
    ax.bar(x, after, width=0.4, label='After DRL', align='edge')

    ax.set_xlabel('Metrics')
    ax.set_ylabel('Values')
    ax.set_title('Network Performance Before and After DRL')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics)
    ax.legend()

    plt.savefig('network_performance.png')
    plt.show()

if __name__ == '__main__':
    plot_metrics()

