from signal_information import SignalInformation

class Node():
    def __init__(self, node):
        self._label = node['label']
        self._position = node['position']
        self._connected_nodes = node['connected_nodes']
        self._successive = {}

    @property
    def label(self):
        return self._label
    
    @label.setter
    def label(self, label):
        self._label = label

    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, position):
        self._position = position

    @property
    def connected_nodes(self):
        return self._connected_nodes
    
    @connected_nodes.setter
    def connected_nodes(self, connected_nodes):
        self._connected_nodes = connected_nodes

    @property
    def successive(self):
        return self._successive
    
    @successive.setter
    def successive(self, successive):
        self._successive = successive

    def propagate(self, signal: SignalInformation, occupate = False):
        if len(signal.path) > 1:
            line_label = signal.path[:2]
            line = self.successive[line_label]
            signal.next()
            signal = line.propagate(signal, occupate)
        
        return signal
