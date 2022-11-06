from network import Network

net = Network('s237002.json')
net.find_best_snr(net.nodes['A'], net.nodes['B'])
#net.find_best_latency(net.nodes[0], net.nodes[1])
#net.draw()
#paths = net.find_paths('A', 'B')