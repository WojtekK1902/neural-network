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
from neuralnetwork.Grossberg import Grossberg
from neuralnetwork.Backpropagation import Backpropagation
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

def liniowa_der(self, x):
    return 1

def progowa_der(self, x):
    return 0

def sigmoida_der(self, x):
    return math.e**(-x)/(1+math.e**(-x))**2


FUNCTIONS = {"l": liniowa, "p": progowa, "s" : sigmoida}
DER_FUNCTIONS = {"l": liniowa_der, "p": progowa_der, "s" : sigmoida_der}

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
        l = f.readline().strip().split()
        if l[0] != 'b' and l[-1] != 'bp':
            raise FileFormatException(f.tell())
        if l[-1] == 'bp':
            conf_file = f.readline().strip()
            if not conf_file:
                raise FileFormatException(f.tell())
            layer = Backpropagation(conf_file)
            network.conf_file = conf_file
            layer.bias = map(lambda x: x*(-1.0), map(float, l[1:-1]))
        else:
            layer = StandardLayer()
            layer.bias = map(lambda x: x*(-1.0), map(float, l[1:]))
        network.layers.append(layer)
        for i in range(network.inputs):
            neuron = Neuron()
            neuron.f = types.MethodType(liniowa, neuron)
            neuron.der = types.MethodType(DER_FUNCTIONS["l"], neuron)
            l = f.readline().strip().split()
            if not l:
                raise FileFormatException(f.tell())
            neuron.weights = self.read_weights(l)
            network.layers[-1].neurons.append(neuron)
        if isinstance(layer, Backpropagation):
            layer.prev_change = [[0.0 for w in n.weights] for n in layer.neurons]

        return network

    def create_hidden_layers(self, network, f):
        for i in range(len(network.hidden)):
            l = f.readline().strip()
            if l:
                raise FileFormatException(f.tell())
            l = f.readline().strip().split()
            if l[0] != 'b' or (l[-1] not in FUNCTIONS.keys() and (l[-1] != 'koh' and l[-1] != 'gros' and l[-1] != 'bp')):
                raise FileFormatException(f.tell())

            layer = None
            neuron = Neuron()
            deriv = None
            if l[-1] == 'koh':
                conf_file = f.readline().strip()
                if not conf_file:
                    raise FileFormatException(f.tell())
                layer = Kohonen(conf_file)
                network.conf_file = conf_file
                func = types.MethodType(liniowa, neuron)
            elif l[-1] == 'gros':
                layer = Grossberg(network.conf_file)
                l = f.readline().strip().split()
                func = types.MethodType(FUNCTIONS[l[-1]], neuron)
                deriv = types.MethodType(DER_FUNCTIONS[l[-1]], neuron)
            elif l[-1] == 'bp':
                if network.conf_file == None:
                    conf_file = f.readline().strip()
                    network.conf_file = conf_file
                layer = Backpropagation(network.conf_file)
                l = f.readline().strip().split()
                func = types.MethodType(FUNCTIONS[l[-1]], neuron)
                deriv = types.MethodType(DER_FUNCTIONS[l[-1]], neuron)
            else:
                layer = StandardLayer()
                func = types.MethodType(FUNCTIONS[l[-1]], neuron)
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
                neuron.der = deriv
                neuron.weights = self.read_weights(line)
                network.layers[-1].neurons.append(neuron)
            if isinstance(layer, Backpropagation):
                layer.prev_change = [[0.0 for w in n.weights] for n in layer.neurons]
                
        return network

    def create_output_layer(self, network, f):
        l = f.readline().strip()
        if l not in FUNCTIONS.keys() and (l != 'koh' and l != 'gros' and l!= 'bp'):
            raise FileFormatException(f.tell())

        layer = None
        neuron = Neuron()
        deriv = None
        if l == 'koh':
            conf_file = f.readline().strip()
            if not conf_file:
                raise FileFormatException(f.tell())
            layer = Kohonen(conf_file)
            network.conf_file = conf_file
            func = types.MethodType(liniowa, neuron)
        elif l == 'gros':
            layer = Grossberg(network.conf_file)
            l = f.readline().strip().split()
            func = types.MethodType(FUNCTIONS[l[-1]], neuron)
            deriv = types.MethodType(DER_FUNCTIONS[l[-1]], neuron)
        elif l == 'bp':
            layer = Backpropagation(network.conf_file)
            l = f.readline().strip().split()
            func = types.MethodType(FUNCTIONS[l[-1]], neuron)
            deriv = types.MethodType(DER_FUNCTIONS[l[-1]], neuron)
        else:
            layer = StandardLayer()
            func = types.MethodType(FUNCTIONS[l], neuron)
        network.layers.append(layer)
        for i in range(network.outputs):
            neuron = Neuron()
            neuron.f = func
            neuron.der = deriv
            network.layers[-1].neurons.append(neuron)
        if isinstance(layer, Backpropagation):
            layer.prev_change = [[0.0 for w in n.weights] for n in layer.neurons]
            
        return network
