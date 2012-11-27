import random
import math

class Kohonen(object):
    def __init__(self, conf):
        self.alfa = conf.alfa
        self.r = conf.r
        self.width = conf.width
        self.height = conf.height
        self.output_width = conf.output_width
        self.output_height = conf.output_height
        self.outputs = self.output_width * self.output_height
        self.freq = [1.0/self.outputs for i in range(self.outputs)]
        self.beta = conf.beta
        self.neighbourhood = conf.neighbourhood
        self.conscience = conf.conscience

    def initialize(self):
        random.seed()
        self.weights = [[[random.random() for i in range(self.width)] for j in range(self.height)] for k in range(self.outputs)]
        self.print_network()

    #obliczanie odleglosci
    def G(self, win, k):
        win_x = win % self.output_width
        win_y = win/self.output_width
        k_x = k % self.output_width
        k_y = k/self.output_width

        if math.sqrt((win_x - k_x)**2 + (win_y-k_y)**2) < self.r:
            return 1.0
        return 0.0

    def update_weights(self, pict, win):
        if self.neighbourhood == True:
            for k in range(self.outputs):
                for j in range(self.height):
                    for i in range(self.width):
                        self.weights[k][j][i] += self.alfa*self.G(win, k)*(pict[j][i]-self.weights[k][j][i])
        else:
            for j in range(self.height):
               for i in range(self.width):
                   self.weights[win][j][i] += self.alfa*(pict[j][i]-self.weights[win][j][i])

    def adjust_dist(self, dist, k):
        bias = self.outputs * self.freq[k] - 1
        return dist + bias

    def update_freqs(self, win):
        for k in range(self.outputs):
            if k == win:
                self.freq[k] += self.beta*(1.0 - self.freq[k])
            else:
                self.freq[k] += self.beta*(0.0 - self.freq[k])

    def winner(self, pict):
        min_dist = float('infinity')
        min_dist_ind = -1
        for k, w in enumerate(self.weights):
            s = 0.0
            for j in range(self.height):
                for i in range(self.width):
                    s += (w[j][i] - pict[j][i])**2
            dist = math.sqrt(s)
            if self.conscience == True:
                dist = self.adjust_dist(dist, k)
            if dist < min_dist:
                min_dist = dist
                min_dist_ind = k
        return min_dist_ind

    def learn(self, X, epochs=32000):
        for i in range(4):
            print 'alfa =', self.alfa
            print 'r =', self.r
            for e in range(epochs/4):
                for pict in X:
                    win = self.winner(pict)
                    if self.conscience == True:
                        self.update_freqs(win)
                    self.update_weights(pict, win)
            self.alfa /= 2
            #self.r -= 2
        self.print_network()

    def run(self, pict):
        return self.winner(pict)

    def print_network(self):
        for k in range(self.outputs):
            print
            for j in range(self.height):
                wagi = ''
                for i in range(self.width):
                    wagi += str(self.weights[k][j][i]) + ' '
                print wagi
                print
