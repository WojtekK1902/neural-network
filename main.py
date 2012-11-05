import math
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
    return x/(1+ math.e**(-x))


FUNCTIONS = {"l": liniowa, "p": progowa, "s" : sigmoida  }


if __name__ == '__main__':
    try:
        if len(sys.argv) < 2:
            print "Brakuje pliku :("
            sys.exit(1)
        f = open(sys.argv[1],'r')
        line = f.readline().strip().split()
        if len(line) < 2 or len(line) > 3:
            raise FileFormatException(f.tell())
        network = Network()
        network.inputs = int(line[0])
        network.outputs = int(line[len(line)-1])
        network.hidden = len(line) - 2
        print 'Liczba wejsc: ' + str(network.inputs)
        print 'Liczba warstw ukrytych: ' + str(network.hidden)
        print 'Liczba wyjsc: ' + str(network.outputs)

        #warstwa wejsciowa:
        l = f.readline().strip()
        if l:
            raise FileFormatException(f.tell())
        layer = Layer()
        layer.bias = (-1.0)*float(f.readline().strip())
        network.layers.append(layer)
        for i in range(network.inputs):
            neuron = Neuron()
            neuron.f = types.MethodType(liniowa, neuron)
            l = f.readline().strip().split()
            if not l:
                raise FileFormatException(f.tell())
            neuron.weights = map(float, l)
            network.layers[-1].neurons.append(neuron)

        #warstwy ukryte:
        for i in range(network.hidden):
            l = f.readline().strip()
            if l:
                raise FileFormatException(f.tell())
            layer = Layer()
            layer.bias = (-1.0)*float(f.readline().strip())
            network.layers.append(layer)
            line = f.readline().strip().split()
            if not line:
                raise FileFormatException(f.tell())
            neurons_count = 0
            while line:
                neuron = Neuron()
                l = line[:-1]
                if neurons_count == 0:
                    neurons_count = len(l)
                if len(l) != neurons_count:
                    raise FileFormatException(f.tell())
                neuron.weights = map(float, l)
                neuron.f = types.MethodType(FUNCTIONS[line[-1]], neuron)
                network.layers[-1].neurons.append(neuron)
                line = f.readline().strip().split()

        if(network.hidden == 0): #ugly hack :/
            f.readline()

        #warstwa wyjsciowa:
        layer = Layer()
        network.layers.append(layer)
        for i in range(network.outputs):
            neuron = Neuron()
            neuron.f = types.MethodType(FUNCTIONS[f.readline().strip()], neuron)
            network.layers[-1].neurons.append(neuron)
            
        f.close()

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
