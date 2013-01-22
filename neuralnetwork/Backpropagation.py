import random
import math
import types
from neuralnetwork.Layer import Layer

class Backpropagation(Layer):
    def __init__(self, conf_file):
        super(Backpropagation, self).__init__()
        exec("import "+ conf_file + " as conf")
        self.learning_rates = conf.bp_learning_rates
        self.momenta = conf.momenta
        self.prev_change = []

    def update_learning_rate(self, epoch):
        if epoch > self.learning_rates[self.current_stage][0]:
            info = 'Backpropagation: learning_rate = ' + str(self.learning_rates[self.current_stage][1])
            self.current_stage += 1
            info += ' => learning_rate = ' + str(self.learning_rates[self.current_stage][1])
            print info
        
    def compute_input(self, prev_neurons):
        for neuron in prev_neurons:
            for index, weight in enumerate(neuron.weights):
                self.neurons[index].input += weight * neuron.compute_output()

    def learn(self, weights, epoch, teachers, deltas, vec=None, winner=None):
        self.update_learning_rate(epoch)
        for i in range(len(weights)):
            for j in range(len(weights[i])):
                old_weight = weights[i][j]
                weights[i][j] +=  self.learning_rates[self.current_stage][1] * deltas[i] * self.neurons[j].compute_output() + self.momenta[self.current_stage][1] * self.prev_change[j][i]
                self.prev_change[j][i] = weights[i][j] - old_weight

        for i in range(len(self.bias)):
            old_bias = self.bias[i]
            self.bias[i] += self.learning_rates[self.current_stage][1] * deltas[i] + self.momenta[self.current_stage][1] * self.prev_bias_change[i]
            self.prev_bias_change[i] = self.bias[i] - old_bias
            
        return weights

    def print_layer(self, prev_neurons):
        w_str = '\tWagi:\t'
        weights = [list(el) for el in zip(*[n.weights for n in prev_neurons])]
        for w in weights:
            for w_val in w:
                w_str += '%.2f   ' % w_val
            w_str += '\n\t\t'
        #for n in self.neurons:
        #    print 'Delta:', n.delta
        print w_str
            
