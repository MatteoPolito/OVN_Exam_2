class SignalInformation():
    def __init__(self, power, path):
        self._power = power
        self._path = path
        self._noise = 0
        self._latency = 0
        self.propagationStopped = False

    @property
    def power(self):
        return self._power
    
    @power.setter
    def power(self, power):
        self._power = power

    @property
    def path(self):
        return self._path
    
    @path.setter
    def path(self, path):
        self._path = path

    @property
    def noise(self):
        return self._noise
    
    @noise.setter
    def noise(self, noise):
        self._noise = noise

    @property
    def latency(self):
        return self._latency
    
    @latency.setter
    def latency(self, latency):
        self._latency = latency

    def add_noise(self, inc):
        self.noise = self.noise + inc

    def add_latency(self, inc):
        self.latency = self.latency + inc

    def next(self):
        self.path = self.path[1:]
    
    
class Lightpath(SignalInformation):
    def __init__(self, power, path, channel):
        super().__init__(power, path)
        self._channel = channel # Integer: Indicates frequency slot the signal occupies when is propagated
        
    @property
    def channel(self):
        return self._channel
    
    @channel.setter
    def channel(self, channel):
        self._channel = channel