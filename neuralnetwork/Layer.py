class Layer(object):
    def __init__(self):
        self.bias = []
        self.neurons = []

    def learn(self, weights):
        pass

    def update_parameters(self):
        pass

    def compute_input(self, prev_neurons):
        raise Exception('Implement me!')

    def print_layer(self, prev_neurons):
        for n in layer.prev_neurons:
            print n.weights
