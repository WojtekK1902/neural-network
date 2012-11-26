from Layer import Layer

class StandardLayer(Layer):

    def compute_input(self, prev_neurons):
        for neuron in layer.prev_neurons:
            for index, weight in enumerate(neuron.weights):
                self.neurons[index].input += weight * neuron.compute_output()
