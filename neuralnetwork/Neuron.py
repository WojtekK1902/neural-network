class Neuron(object):
    def __init__(self):
        self.weights = []
        self.f = None
        self.input = 0.0

    def compute_output(self):
        return self.f(self.input)
