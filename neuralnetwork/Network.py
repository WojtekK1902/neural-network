class Network(object):
    def __init__(self):
        self.inputs = 0
        self.outputs = 0
        self.hidden = 0
        self.layers = []

    def compute(self, input):
	for x, neuron in zip(input, self.layers[0].neurons):
		neuron.input += x

	for layer_index, layer in enumerate(self.layers[:-1]):
		for neuron in layer.neurons:
			for index, weight in enumerate(neuron.weights):
				self.layers[layer_index + 1].neurons[index].input += weight * neuron.compute_output()

	for l in self.layers:
		print "Warstwa " + str(l.bias)
		for n in l.neurons:
			print n.input

	return map(lambda n: n.compute_output(), self.layers[-1].neurons)
