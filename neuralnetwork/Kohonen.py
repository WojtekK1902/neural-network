import random
import math
from neuralnetwork.Layer import Layer

class Kohonen(Layer):
    def __init__(self, conf_file):
        super(Kohonen, self).__init__()
        exec("import "+ conf_file + " as conf")
        self.alfas = conf.alfas
        self.r = conf.r
        self.output_width = conf.output_width
        self.output_height = conf.output_height
        self.outputs = self.output_width * self.output_height
        self.freq = [1.0/self.outputs for i in range(self.outputs)]
        self.beta = conf.beta
        self.neighbourhood = conf.neighbourhood
        self.conscience = conf.conscience

    #obliczanie odleglosci
    def G(self, win, k):
        win_x = win % self.output_width
        win_y = win/self.output_width
        k_x = k % self.output_width
        k_y = k/self.output_width

        if math.sqrt((win_x - k_x)**2 + (win_y-k_y)**2) < self.r:
            return 1.0
        return 0.0

    def update_weights(self, vec, win, weights):
        if self.neighbourhood == True:
            for k, w in enumerate(weights):
                for i in range(len(w)):
                        weights[k][i] += self.alfas[self.current_stage][1]*self.G(win, k)*(vec[i]-weights[k][i])
        else:
            for i in range(len(weights[win])):
                   weights[win][i] += self.alfas[self.current_stage][1]*(vec[i]-weights[win][i])
                   
        return weights

    def adjust_dist(self, dist, k):
        bias = self.outputs * self.freq[k] - 1
        return dist + bias

    def update_freqs(self, win):
        for k in range(self.outputs):
            if k == win:
                self.freq[k] += self.beta*(1.0 - self.freq[k])
            else:
                self.freq[k] += self.beta*(0.0 - self.freq[k])

    def winner(self, vec, weights, run=False):
        min_dist = float('infinity')
        min_dist_ind = -1
        for k, w in enumerate(weights):
            s = 0.0
            for val_w, val_vec in zip(w, vec):
                s += (val_w - val_vec)**2
            dist = math.sqrt(s)
            if run == False and self.conscience == True:
                dist = self.adjust_dist(dist, k)
            if dist < min_dist:
                min_dist = dist
                min_dist_ind = k
        return min_dist_ind

    def learn(self, weights, epoch, vec, teacher=None, winner=None, deltas=None):
        if epoch > self.alfas[self.current_stage][0]:
            info = 'Kohonen: alfa = ' + str(self.alfas[self.current_stage][1])
            self.current_stage += 1
            info += ' => alfa = ' + str(self.alfas[self.current_stage][1])
            print info
        win = self.winner(vec, weights)
        if self.conscience == True:
            self.update_freqs(win)
        weights = self.update_weights(vec, win, weights)
        return [weights, win]

    def compute_input(self, prev_neurons):
        weights = [list(el) for el in zip(*[n.weights for n in prev_neurons])]
        vec = [n.compute_output() for n in prev_neurons]
        self.neurons[self.winner(vec, weights, True)].input = 1.0

    def print_layer(self, prev_neurons):
        w_str = '\tWagi:\t'
        weights = [list(el) for el in zip(*[n.weights for n in prev_neurons])]
        for w in weights:
            for w_val in w:
                w_str += '%.2f   ' % w_val
            w_str += '\n\t\t'
        print w_str
            
