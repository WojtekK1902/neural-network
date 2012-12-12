import random
import math
from neuralnetwork.Layer import Layer

class Grossberg(Layer):
    def __init__(self, conf_file):
        super(Grossberg, self).__init__()
        exec("import "+ conf_file + " as conf")
        self.learning_rate = conf.learning_rate
        self.outputs = conf.outputs

##TODO
##    def update_parameters(self):
##        print 'alfa =', self.alfa
##        self.alfa /= 2
##
##    def update_weights(self, vec, win, weights):
##        if self.neighbourhood == True:
##            for k, w in enumerate(weights):
##                for i in range(len(w)):
##                        weights[k][i] += self.alfa*self.G(win, k)*(vec[i]-weights[k][i])
##        else:
##            for i in range(len(weights[win])):
##                   weights[win][i] += self.alfa*(vec[i]-weights[win][i])
##                   
##        return weights
##
##    def learn(self, weights, vec):
##        win = self.winner(vec, weights)
##        if self.conscience == True:
##            self.update_freqs(win)
##        weights = self.update_weights(vec, win, weights)
##        return weights
##
##    def compute_input(self, prev_neurons):
##        weights = [list(el) for el in zip(*[n.weights for n in prev_neurons])]
##        vec = [n.compute_output() for n in prev_neurons]
##        self.neurons[self.winner(vec, weights)].input = 1.0
##
##    def print_layer(self, prev_neurons):
##        w_str = '\tWagi:\t'
##        weights = [list(el) for el in zip(*[n.weights for n in prev_neurons])]
##        for w in weights:
##            for w_val in w:
##                w_str += '%.2f   ' % w_val
##            w_str += '\n\t\t'
##        print w_str
            
