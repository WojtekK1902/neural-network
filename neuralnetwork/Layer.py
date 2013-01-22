class Layer(object):
    def __init__(self):
        self.bias = []
        self.neurons = []
        self.current_stage = 0

    def learn(self, weights, epoch, vec, teacher, winner, deltas):
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
