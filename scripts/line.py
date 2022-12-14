from signal_information import SignalInformation

class Line():
    def __init__(self, line):
        self._label = line['label']
        self._length = line['length']
        self._successive = {}

    @property
    def label(self):
        return self._label
    
    @label.setter
    def label(self, label):
        self._label = label

    @property
    def length(self):
        return self._length
    
    @length.setter
    def length(self, length):
        self._length = length

    @property
    def successive(self):
        return self._successive
    
    @successive.setter
    def successive(self, successive):
        self._successive = successive

    def latency_generation(self):
        c = 299792458
        return self.length / (c * 2/3)

    def noise_generation(self, sig_power):
        return sig_power / (2 * self.length)

    def propagate(self, signal: SignalInformation):
        latency = self.latency_generation()
        signal.add_latency(latency)

        noise = self.noise_generation(signal.power)
        signal.add_noise(noise)

        node = self.successive[signal.path[0]]
        signal = node.propagate(signal)
        return signal
