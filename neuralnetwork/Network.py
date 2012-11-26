from Kohonen import Kohonen
from neuralnetwork.Layer import Layer

class Network(object):
    def __init__(self):
        self.inputs = 0
        self.outputs = 0
        self.hidden = 0
        self.layers = []
        self.epochs = 0
        self.trainig_file = None

    def compute(self, input):
        for x, neuron in zip(input, self.layers[0].neurons):
            neuron.input += x

        for layer_index, layer in enumerate(self.layers[:-1]):
            if len(layer.bias) != 0:
                for i, neuron in enumerate(self.layers[layer_index+1].neurons):
                    neuron.input += layer.bias[i]
            self.layers[layer_index + 1].compute_input(layer.neurons)
            

        return map(lambda n: n.compute_output(), self.layers[-1].neurons)

    def read_training_file(self):
        f = open(self.training_file, 'r')
        X, w = [], []
        for line in f:
            l = line.strip().split()
            if len(l[0].split('&')) == 1:
                if len(w) > 0:
                    X.append(w)
                w = []
            l[0] = l[0].strip('&')
            w.extend(map(float, l))
        X.append(w)
        return X

    def clear_network(self):
        for layer in self.layers:
            for neuron in layer.neurons:
                neuron.input = 0

    def learn(self):
        X = self.read_training_file()
        print X

        for k in range(4):
            for e in range(self.epochs/4):
                for vec in X:
                    self.compute(vec)
                    for i, layer in enumerate(self.layers[1:]):
                        new_weights = layer.learn([list(el) for el in zip(*[n.weights for n in self.layers[i].neurons])], [n.compute_output() for n in self.layers[i].neurons])
                        new_weights = [list(el) for el in zip(*new_weights)]
                        for j, n in enumerate(self.layers[i].neurons):
                            n.weights = new_weights[j]
                        self.clear_network()
            for layer in self.layers:
                layer.update_parameters()

    def print_network(self):
        for i, layer in enumerate(self.layers[1:]):
            print
            print 'Warstwy' + str(i+1) + '-' + str(i+2) + ':'
            layer.print_layer(self.layers[i].neurons)
            
        
