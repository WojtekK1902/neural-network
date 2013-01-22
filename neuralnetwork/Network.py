from Kohonen import Kohonen
from Grossberg import Grossberg
from Backpropagation import Backpropagation
from neuralnetwork.Layer import Layer

class Network(object):
    def __init__(self):
        self.inputs = 0
        self.outputs = 0
        self.hidden = 0
        self.layers = []
        self.epochs = 0
        self.trainig_file = None
        self.conf_file = None

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
        for line in f:
            if line[0] == '!':
                continue
            l = line.strip().split()
            if len(l[0].split('&')) == 1:
                if len(w) > 0:
                    X.append(w)
                w = []
            l[0] = l[0].strip('&')
            w.extend(map(float, l))
            if len(w) > len(self.layers[0].neurons):
                teachers.append(w[len(self.layers[0].neurons):])
                w = w[:len(self.layers[0].neurons)]
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
                self.compute_deltas(teachers[vec_i])
                for i, layer in enumerate(self.layers):
                    if isinstance(layer, Kohonen):
                        [new_weights, winner] = layer.learn([list(el) for el in zip(*[n.weights for n in self.layers[i].neurons])], e, [n.compute_output() for n in self.layers[i].neurons])
                    elif isinstance(layer, Grossberg):
                        new_weights = layer.learn([list(el) for el in zip(*[n.weights for n in self.layers[i].neurons])], e, teachers[vec_i], winner)
                    elif isinstance(layer, Backpropagation):
                        deltas = None
                        if i < len(self.layers) - 1:
                            deltas = [n.delta for n in self.layers[i+1].neurons]
                        new_weights = layer.learn([list(el) for el in zip(*[n.weights for n in self.layers[i].neurons])], e, teachers[vec_i], deltas)
                    if new_weights != None and len(new_weights) > 0:
                        new_weights = [list(el) for el in zip(*new_weights)]
                        for j, n in enumerate(self.layers[i].neurons):
                            n.weights = new_weights[j]
                self.clear_network()

    def compute_deltas(self, teachers):
        for i, n in enumerate(self.layers[-1].neurons):
            n.delta = n.compute_deriv()*(teachers[i]-n.compute_output())
        for i in range(len(self.layers)-2,0,-1):
            epsilons = [0.0 for n in self.layers[i].neurons]
            for k, n in enumerate(self.layers[i].neurons):
                for j, n_next in enumerate(self.layers[i+1].neurons):
                    epsilons[k] += n_next.delta * n.weights[j]

            for k, n in enumerate(self.layers[i].neurons):
                n.delta = epsilons[k] * n.compute_deriv()
            

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
            
        
