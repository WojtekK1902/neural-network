import math
import types
from neuralnetwork.Neuron import Neuron
from neuralnetwork.Layer import Layer
from neuralnetwork.Network import Network


def liniowa(self, x):
    return x

def progowa(self, x):
    if x > 0:
        return 1
    else:
        return 0

def sigmoida(self, x):
    return x/(1+ math.e**(-x))


FUNCTIONS = {"l": liniowa, "p": progowa, "s" : sigmoida  }


if __name__ == '__main__':
    f = open('configuration.data','r')
    line = f.readline().strip().split()
    network = Network()
    network.inputs = int(line[0])
    network.outputs = int(line[len(line)-1])
    network.hidden = len(line) - 2
    print 'Liczba wejsc: ' + str(network.inputs)
    print 'Liczba warstw ukrytych: ' + str(network.hidden)
    print 'Liczba wyjsc: ' + str(network.outputs)

    #warstwa wejsciowa:
    f.readline()
    layer = Layer()
    layer.bias = float(f.readline().strip())
    network.layers.append(layer)
    for i in range(network.inputs):
        neuron = Neuron()
        neuron.weights = map(float, f.readline().strip().split())
        network.layers[-1].neurons.append(neuron)

    #warstwy ukryte:
    for i in range(network.hidden):
        f.readline()
        layer = Layer()
        layer.bias = float(f.readline().strip())
        network.layers.append(layer)
        line = f.readline().strip().split()
        while line:
            neuron = Neuron()
            neuron.weights = map(float, line[:-1])
            neuron.f = types.MethodType(FUNCTIONS[line[-1]], neuron)
            network.layers[-1].neurons.append(neuron)
            line = f.readline().strip().split()

    #warstwa wyjsciowa:
    layer = Layer()
    layer.bias = float(f.readline().strip())
    network.layers.append(layer)
    for i in range(network.outputs):
        neuron = Neuron()
        neuron.f = types.MethodType(FUNCTIONS[f.readline().strip()], neuron)
        network.layers[-1].neurons.append(neuron)
        

##    for line in f:
##        if not line.strip():
##            network.layers.append(Layer())
##        else:
##            neuron = Neuron()
##            input = line.strip().split()
##            if len(network.layers) > 1:
##                neuron.weights = map(float, input[:-2])
##                neuron.f = types.MethodType(FUNCTIONS[input[-2]], neuron)
##            else:
##                neuron.weights = map(float, input[:-1])
##            neuron.bias = input[-1]
##            network.layers[-1].neurons.append(neuron)
##
##    network.layers.append(Layer()) #warstwa wyjsciowa
##    for i in range(0,network.outputs):
##        network.layers[-1].neurons.append(Neuron())

    for l in network.layers:
        print "Warstwa " + str(l.bias)
        for n in l.neurons:
            print n.weights
            print n.f

    f.close()
