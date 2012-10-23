from neuralnetwork.Neuron import Neuron
from neuralnetwork.Layer import Layer
from neuralnetwork.Network import Network

if __name__ == '__main__':
    neuron = Neuron()
    layer = Layer()
    

    f = open('configuration.data','r')
    line = f.readline().strip().split()
    network = Network()
    network.inputs = int(line[0])
    network.outputs = int(line[len(line)-1])
    network.hidden = len(line) - 2
    print 'Liczba wejsc: ' + str(network.inputs)
    print 'Liczba warstw ukrytych: ' + str(network.hidden)
    print 'Liczba wyjsc: ' + str(network.outputs)
    f.close()
