class Layer(object):
    def __init__(self):
        self.bias = []
        self.neurons = []

    def learn(self, weights, vec, epoch):
        pass

    def compute_input(self, prev_neurons):
        raise Exception('Implement me!')

    def print_layer(self, prev_neurons):
        n_str = '\tWagi:\t'
        for n in prev_neurons:
            for w in n.weights:
                n_str += '%.3f   ' % w
            n_str += '\n\t\t'
        print n_str
