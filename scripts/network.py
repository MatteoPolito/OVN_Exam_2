import json
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from node import Node
from line import Line
from signal_information import SignalInformation
from connection import Connection

class Network():
    def __init__(self, json_path):
        node_json = json.load(open(json_path, 'r'))
        self._nodes = {}
        self._lines = {}
        for node_label in node_json:
            # Creating Node
            nodeData = node_json[node_label]
            nodeData['label'] = node_label
            node = Node(nodeData)
            self.nodes[node_label] = node
            # Creating Lines
            for linked_label in node.connected_nodes:
                lineData = {}
                lineData['label'] = node_label + linked_label
                n1_pos = np.array(node.position)
                n2_pos = np.array(node_json[linked_label]['position'])
                lineData['length'] = math.sqrt(math.pow(n1_pos[0] - n2_pos[0], 2) + math.pow(n1_pos[1] - n2_pos[1], 2))
                line = Line(lineData)
                self.lines[line.label] = line
        
        self.weighted_paths = self.createDataframe()

    @property
    def nodes(self):
        return self._nodes

    @property
    def lines(self):
        return self._lines

    def draw(self):
        for n_label in self.nodes:
            n0 = self.nodes[n_label]
            x0 = n0.position[0]
            y0 = n0.position[1]
            plt.plot(x0, y0, 'o', markersize=10, color='red', zorder=10)
            plt.text(x0 + 5000, y0 + 5000, n_label, zorder=15)
            for linked_label in n0.connected_nodes:
                n1 = self.nodes[linked_label]
                x1 = n1.position[0]
                y1 = n1.position[1]
                plt.plot([x0, x1], [y0, y1], color='grey', zorder=0, markersize=0.5)
        plt.title('Network - Topology')
        plt.show()

    def find_paths(self, nodeName1: str, nodeName2: str):
        node1 = self.nodes[nodeName1]
        node2 = self.nodes[nodeName2]
        result = []
        self.cyclicFind(node1, node2, '', result)
        return result

    def cyclicFind(self, curNode: Node, endNode: Node, path, result):
        path += curNode.label
        # if i reached the end node i can return the found path
        if(curNode.label == endNode.label):
            #print("End Reached!", path)
            result.append(path)

        # i will try all possible ways in the adjacents nodes
        for way in curNode.connected_nodes:
            # if node hasn't already been considered in this path i will calculate new path
            if not Network.nodeIsInPath(way, path):
                self.cyclicFind(self.nodes[way], endNode, path, result)

    @staticmethod
    def nodeIsInPath(nodeLabel, path):
        for n in path:
            if n == nodeLabel:
                return True
        return False

    def connect(self):
        for lineKey in self.lines:
            # from the first letter of the line's label i will get the starting node. I will assign it to the line and viceversa
            line = self.lines[lineKey]
            n1 = self.nodes[line.label[0]]
            n2 = self.nodes[line.label[1]]
            n1.successive[line.label] = line
            line.successive[n1.label] = n1
            line.successive[n2.label] = n2

    def propagate(self, signal: SignalInformation) -> SignalInformation:
        path = signal.path
        n = self.nodes[path[0]] # Starting node
        signal = n.propagate(signal)
        return signal

    def createDataframe(self) -> pd.DataFrame:
        self.connect()
        pairs = []
        node_labels = self.nodes.keys()
        for n1 in node_labels:
            for n2 in node_labels:
                if n1 != n2:
                    pairs.append(n1+n2)
        
        df = pd.DataFrame()
        paths = []
        latencies = []
        noises = []
        snrs = []

        for pair in pairs:
            for path in self.find_paths(pair[0], pair[1]):
                path_string = ''
                for node in path:
                    path_string += node + '->'
                paths.append(path_string[:-2]) # removing last '->'

                signal = SignalInformation(1, path)
                signal = self.propagate(signal)
                latencies.append(signal.latency)
                noises.append(signal.noise)
                snrs.append(10 * np.log10(signal.power/signal.noise))
        # Populating Dataframe
        df['path'] = paths
        df['latency'] = latencies
        df['noise'] = noises
        df['snr'] = snrs
        return df
    
    def find_best_snr(self, node1: Node, node2: Node):
        paths = self.filterPathsByStartEnd(node1.label, node2.label)
        filtered = self.weighted_paths.loc[self.weighted_paths['path'].isin(paths)]
        print(filtered)
        best = filtered['snr'].max()
        print(best)
    
    def find_best_latency(self, node1: Node, node2: Node):
        paths = self.filterPathsByStartEnd(node1.label, node2.label)
        filtered = self.weighted_paths.loc[self.weighted_paths['path'].isin(paths)]
        print(filtered)
        best = filtered['latency'].min()
        print(best)
        
    def filterPathsByStartEnd(self, start, end):
       return [path for path in self.weighted_paths['path'].values
                 if (path[0] == start) and (path[-1] == end)]
       
    def stream(self, connections: Connection, best='latency'):
        streamed_connections = []
        for connection in connections:
            input_node = connection.input_node
            output_node = connection.output_node
            signal_power = connection.signal_power
            self.weighted_paths(signal_power)
            if best == 'latency':
                path = self.find_best_latency(input_node, output_node)
            elif best == 'snr':
                path = self.find_best_snr(input_node, output_node)
            else:
                print('ERROR: best input not recognized. Value:', best)
                break
            signal = SignalInformation(signal_power, path)
            signal = self.propagate(signal)
            connection.latency = signal.latency
            connection.snr = 10*np.log10(signal_power/signal.noise)
            streamed_connections.append(connection)
        return streamed_connections