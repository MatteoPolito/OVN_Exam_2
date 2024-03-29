import numpy as np
from signal_information import Lightpath

class Connection():
    def __init__(self, input_node, output_node, signal_power) -> None:
        self._input_node = input_node
        self._output_node = output_node
        self._signal_power = signal_power
        self._latency = 0
        self._snr = 0
        
    @property
    def input_node(self):
        return self._input_node
    
    @property
    def output_node(self):
        return self._output_node
    
    @property
    def signal_power(self):
        return self._signal_power
    
    @property
    def latency(self):
        return self._latency
    
    @property
    def snr(self):
        return self._snr
    
    @latency.setter
    def latency(self, latency):
        self._latency = latency
        
    @snr.setter
    def snr(self, snr):
        self._snr = snr