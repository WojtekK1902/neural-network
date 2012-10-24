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

def  sigmoida(self, x):
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

    for line in f:
        if not line.strip():
            network.layers.append(Layer())
        else:
            neuron = Neuron()
            input = line.strip().split()
            neuron.weights = map(float, input[:-2])
            neuron.f = types.MethodType(FUNCTIONS[input[-2]], neuron)
            neuron.bias = input[-1]
            network.layers[-1].neurons.append(neuron)

    network.layers.append(Layer()) #warstwa wyjsciowa
    for i in range(0,network.outputs):
        network.layers[-1].neurons.append(Neuron())

    for l in network.layers:
        print "Warstwa"
        for n in l.neurons:
            print n.weights

    f.close()
