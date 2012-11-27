import math
import random
import re
import types
import sys
from neuralnetwork.Neuron import Neuron
from neuralnetwork.Layer import Layer
from neuralnetwork.StandardLayer import StandardLayer
from neuralnetwork.Network import Network
from neuralnetwork.Kohonen import Kohonen
from neuralnetwork.FileFormatException import FileFormatException


def liniowa(self, x):
    return x

def progowa(self, x):
    if x > 0:
        return 1
    else:
        return 0

def sigmoida(self, x):
    return 1/(1+ math.e**(-x))


FUNCTIONS = {"l": liniowa, "p": progowa, "s" : sigmoida  }

class NetworkCreator(object):

    def read_weights(self, line):
        weights = []
        for weight in line:
            try:
                weights.append(float(weight))
            except ValueError:
                count = int(weight.split("[")[0])
                lower_bound = float(weight.split("[")[1].split(":")[0])
                upper_bound = float(weight.split(":")[1].split("]")[0])
                for i in range(count):
                    weights.append(random.uniform(lower_bound, upper_bound))
        return weights

    def create_input_layer(self, network, f):
        l = f.readline().strip()
        if l:
            raise FileFormatException(f.tell())
        layer = StandardLayer()
        l = f.readline().strip().split()
        if l[0] != 'b':
            raise FileFormatException(f.tell())
        layer.bias = map(lambda x: x*(-1.0), map(float, l[1:]))
        network.layers.append(layer)
        for i in range(network.inputs):
            neuron = Neuron()
            neuron.f = types.MethodType(liniowa, neuron)
            l = f.readline().strip().split()
            if not l:
                raise FileFormatException(f.tell())
            neuron.weights = self.read_weights(l)
            network.layers[-1].neurons.append(neuron)

        return network

    def create_hidden_layers(self, network, f):
        for i in range(len(network.hidden)):
            l = f.readline().strip()
            if l:
                raise FileFormatException(f.tell())
            l = f.readline().strip().split()
            if l[0] != 'b' or (l[-1] not in FUNCTIONS.keys() and l[-1] != 'koh'):
                raise FileFormatException(f.tell())

            layer = None
            neuron = Neuron()
            if l[-1] != 'koh':
                layer = StandardLayer()
                func = types.MethodType(FUNCTIONS[l[-1]], neuron)
            else:
                conf_file = f.readline().strip()
                if not conf_file:
                    raise FileFormatException(f.tell())
                layer = Kohonen(conf_file)
                func = types.MethodType(liniowa, neuron)                    
            layer.bias = map(lambda x: x*(-1.0), map(float, l[1:-1]))
            network.layers.append(layer)
            neurons_count = 0
            for j in range(network.hidden[i]):
                line = f.readline().strip().split()
                if not line:
                    raise FileFormatException(f.tell())
                neuron = Neuron()
                if neurons_count == 0:
                    neurons_count = len(line)
                if len(line) != neurons_count:
                    raise FileFormatException(f.tell())
                neuron.f = func
                neuron.weights = self.read_weights(line)
                network.layers[-1].neurons.append(neuron)
                
        return network

    def create_output_layer(self, network, f):
        l = f.readline().strip()
        if l not in FUNCTIONS.keys() and l != 'koh':
            raise FileFormatException(f.tell())

        layer = None
        neuron = Neuron()
        if l != 'koh':
            layer = StandardLayer()
            func = types.MethodType(FUNCTIONS[l], neuron)
        else:
            conf_file = f.readline().strip()
            if not conf_file:
                raise FileFormatException(f.tell())
            layer = Kohonen(conf_file)
            func = types.MethodType(liniowa, neuron)
        network.layers.append(layer)
        for i in range(network.outputs):
            neuron = Neuron()
            neuron.f = func
            network.layers[-1].neurons.append(neuron)
            
        return network
