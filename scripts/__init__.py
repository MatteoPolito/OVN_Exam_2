from network import Network
from random import shuffle
from connection import Connection
import matplotlib.pyplot as plt
import numpy as np

net = Network('s237002.json')
net.plotBitRate_GSNR()
node_labels = list(net.nodes.keys())
connections = []
for i in range(100):
    shuffle(node_labels)
    connection = Connection(node_labels[0], node_labels[-1], 1)
    connections.append(connection)
    
streamed_connections = net.stream(connections)
latencies = [connection.latency for connection in streamed_connections]
plt.hist(latencies, bins=10)
plt.title('Latency Distribution')
plt.show()
latencyAverage = np.array(latencies).mean()

streamed_connections = net.stream(connections, best='snr')
snrs = [connection.snr for connection in streamed_connections]
plt.hist(snrs, bins=10)
plt.title('SNR Distribution')
plt.show()
snrAverage = np.array(snrs).mean()