import math
import types
import sys
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
    if len(sys.argv) < 2:
        print "Brakuje pliku :("
        sys.exit(1)
    f = open(sys.argv[1],'r')
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
        neuron.input = layer.bias
        neuron.f = types.MethodType(liniowa, neuron)
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
            neuron.input = layer.bias
            neuron.weights = map(float, line[:-1])
            neuron.f = types.MethodType(FUNCTIONS[line[-1]], neuron)
            network.layers[-1].neurons.append(neuron)
            line = f.readline().strip().split()

    #warstwa wyjsciowa:
    f.readline()
    layer = Layer()
    layer.bias = float(f.readline().strip())
    network.layers.append(layer)
    for i in range(network.outputs):
        neuron = Neuron()
        neuron.input = layer.bias
        neuron.f = types.MethodType(FUNCTIONS[f.readline().strip()], neuron)
        network.layers[-1].neurons.append(neuron)
        
##    for l in network.layers:
##        print "Warstwa " + str(l.bias)
##        for n in l.neurons:
##            print n.weights
##            print n.f

    f.close()

    input = []
    print
    for i in range(network.inputs):
        input.append(float(raw_input('Input ' + str(i+1) + ': ')))

    print
    print "input: " + str(input)

    for x, neuron in zip(input, network.layers[0].neurons):
        neuron.input += x

    for layer_index, layer in enumerate(network.layers[:-1]):
        for neuron in layer.neurons:
            for index, weight in enumerate(neuron.weights):
                network.layers[layer_index + 1].neurons[index].input += weight * neuron.compute_output()

    for l in network.layers:
        print "Warstwa " + str(l.bias)
        for n in l.neurons:
            print n.input

    output = map(lambda n: n.compute_output(), network.layers[-1].neurons)

    print "odpowiedz sieci: " + str(output)

