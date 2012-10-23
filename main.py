from neuralnetwork.Neuron import Neuron
from neuralnetwork.Layer import Layer
from neuralnetwork.Network import Network

if __name__ == '__main__':
    neuron = Neuron()
    layer = Layer()
    network = Network()
    neuron.powiedzCosOSobie()
    layer.powiedzCosOSobie()
    network.powiedzCosOSobie()

    f = open('configuration.data','r')
    for line in f:
        print line.strip()
    f.close()
