import math
import random
import re
import types
import sys
from neuralnetwork.Neuron import Neuron
from neuralnetwork.Layer import Layer
from neuralnetwork.Network import Network
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


def read_weights(line):
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

if __name__ == '__main__':
    try:
        if len(sys.argv) < 2:
            print "Brakuje pliku :("
            sys.exit(1)
        f = open(sys.argv[1],'r')
        line = f.readline().strip().split()
        if len(line) < 2:
            raise FileFormatException(f.tell())
        network = Network()
        network.inputs = int(line[0])
        network.outputs = int(line[len(line)-1])
        network.hidden = map(int, line[1:-1])
        print 'Liczba wejsc:', str(network.inputs)
        print 'Liczba warstw ukrytych:', str(len(network.hidden))
        print 'Warstwy ukryte:', str(network.hidden)
        print 'Liczba wyjsc:', str(network.outputs)

        #warstwa wejsciowa:
        l = f.readline().strip()
        if l:
            raise FileFormatException(f.tell())
        layer = Layer()
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
            neuron.weights = read_weights(l)
            network.layers[-1].neurons.append(neuron)

        #warstwy ukryte:
        for i in range(len(network.hidden)):
            l = f.readline().strip()
            if l:
                raise FileFormatException(f.tell())
            layer = Layer()
            l = f.readline().strip().split()
            if l[0] != 'b' or l[-1] not in FUNCTIONS.keys():
                raise FileFormatException(f.tell())
            layer.bias = map(lambda x: x*(-1.0), map(float, l[1:-1]))
            func = types.MethodType(FUNCTIONS[l[-1]], neuron)
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
                neuron.weights = read_weights(line)
                neuron.f = func
                network.layers[-1].neurons.append(neuron)


        l = f.readline().strip()
        if l:
            raise FileFormatExcpetion(f.tell())

        #warstwa wyjsciowa:
        layer = Layer()
        network.layers.append(layer)
        func = types.MethodType(FUNCTIONS[f.readline().strip()], neuron)
        for i in range(network.outputs):
            neuron = Neuron()
            neuron.f = func
            network.layers[-1].neurons.append(neuron)
            
        f.close()

        for layer in network.layers:
            print "bias: " + str(layer.bias)
            for neuron in layer.neurons:
                print neuron.weights
#                print neuron.f

        input = []
        print
        for i in range(network.inputs):
            input.append(float(raw_input('Input ' + str(i+1) + ': ')))

        print
        print "input: " + str(input)

        output = network.compute(input)

        print "odpowiedz sieci: " + str(output)
        
    except FileFormatException as e:
        print 'Bad file format at position:', e.pos
