from Kohonen import Kohonen
from Grossberg import Grossberg
from neuralnetwork.Layer import Layer

class Network(object):
    def __init__(self):
        self.inputs = 0
        self.outputs = 0
        self.hidden = 0
        self.layers = []
        self.epochs = 0
        self.trainig_file = None
        self.koh_gros_conf = None

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
        X, w, teachers = [], [], []
        prev = []
        for line in f:
            if line[0] == '!':
                continue
            l = line.strip().split()
            if len(prev) > 0 and len(l) > len(prev):
                teachers.append(l[len(l)/2:])
            if len(l[0].split('&')) == 1:
                if len(w) > 0:
                    X.append(w)
                w = []
            l[0] = l[0].strip('&')
            w.extend(map(float, l))
            prev = l
        X.append(w)
        return [X, [map(float, l) for l in teachers]]

    def clear_network(self):
        for layer in self.layers:
            for neuron in layer.neurons:
                neuron.input = 0

    def learn(self):
        [X, teachers] = self.read_training_file()

        for e in range(self.epochs):
            for vec_i, vec in enumerate(X):
                self.compute(vec)
                for i, layer in enumerate(self.layers[1:]):
                    if isinstance(layer, Kohonen):
                        [new_weights, winner] = layer.learn([list(el) for el in zip(*[n.weights for n in self.layers[i].neurons])], e, [n.compute_output() for n in self.layers[i].neurons])
                    elif isinstance(layer, Grossberg):
                        new_weights = layer.learn([list(el) for el in zip(*[n.weights for n in self.layers[i].neurons])], e, teachers[vec_i], winner)
                    if new_weights != None and len(new_weights) > 0:
                        new_weights = [list(el) for el in zip(*new_weights)]
                        for j, n in enumerate(self.layers[i].neurons):
                            n.weights = new_weights[j]
                self.clear_network()

    def print_network(self):
        for i, layer in enumerate(self.layers[1:]):
            print
            print 'Warstwy ' + str(i+1) + '-' + str(i+2) + ':'
            bias_str = '\tBias:\t'
            if len(self.layers[i].bias) == 0:
                bias_str += '0.0'
            else:
                for b in self.layers[i].bias:
                    bias_str += '%.3f ' % b
            print bias_str
            layer.print_layer(self.layers[i].neurons)
            
        
