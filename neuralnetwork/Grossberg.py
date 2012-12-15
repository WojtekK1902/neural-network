import random
import math
import types
from neuralnetwork.Layer import Layer

class Grossberg(Layer):
    def __init__(self, conf_file):
        super(Grossberg, self).__init__()
        exec("import "+ conf_file + " as conf")
        self.learning_rates = conf.learning_rates
        self.outputs = conf.outputs
        self.current_stage = 0
        self.learn = getattr(self, conf.learning_rule)

    def update_learning_rate(self, epoch):
        if epoch > self.learning_rates[self.current_stage][0]:
            info = 'Grossberg: learning_rate = ' + str(self.learning_rates[self.current_stage][1])
            self.current_stage += 1
            info += ' => learning_rate = ' + str(self.learning_rates[self.current_stage][1])
            print info

    def WidrowHoff(self, weights, epoch, teacher, winner, vec = None):
        self.update_learning_rate(epoch)
        for i in range(len(weights)):
            weights[i][winner] += self.learning_rates[self.current_stage][1]*(teacher[i]-self.neurons[i].compute_output())
        return weights

    def DeltaRule(self, weights, epoch, teacher, winner, vec = None):
        self.update_learning_rate(epoch)
        for i in range(len(weights)):
            weights[i][winner] += self.learning_rates[self.current_stage][1]*(teacher[i]-self.neurons[i].compute_output())*self.neurons[i].compute_deriv()
        return weights
        
    def compute_input(self, prev_neurons):
        for neuron in prev_neurons:
            for index, weight in enumerate(neuron.weights):
                self.neurons[index].input += weight * neuron.compute_output()

    def print_layer(self, prev_neurons):
        w_str = '\tWagi:\t'
        weights = [list(el) for el in zip(*[n.weights for n in prev_neurons])]
        for w in weights:
            for w_val in w:
                w_str += '%.2f   ' % w_val
            w_str += '\n\t\t'
        print w_str
            
