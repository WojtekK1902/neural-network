import random
import math

class Kohonen(object):
    def __init__(self, width=3, height=3, outputs=4):
        #TODO: dodac bias!
        #TODO: ewentualnie ustawianie alfa
        self.alfa = 0.06
        #TODO: dodac ustawianie promienia sasiedztwa
        self.r = 7
        self.width = width
        self.height = height
        self.outputs = outputs

    def initialize(self):
        random.seed()
        self.weights = [[[random.random() for i in range(self.width)] for j in range(self.height)] for k in range(self.outputs)]
        self.print_network()

    #obliczanie odleglosci
    #na razie tylko dla 1D
    def G(self, win, k):
        if abs(win-k) <= self.r:
            return 1.0
        return 0.0

    def update_weights(self, pict, win):
        for k in range(self.outputs):
            for j in range(self.height):
                for i in range(self.width):
                    self.weights[k][j][i] += self.alfa*self.G(win, k)*(pict[j][i]-self.weights[k][j][i])

    def winner(self, pict):
        min_dist = float('infinity')
        min_dist_ind = -1
        for k, w in enumerate(self.weights):
            s = 0.0
            for j in range(self.height):
                for i in range(self.width):
                    s += (w[j][i] - pict[j][i])**2
            dist = math.sqrt(s)
            if dist < min_dist:
                min_dist = dist
                min_dist_ind = k
        return min_dist_ind

    #TODO: czy liczba epok nie powinna byc konfigurowalna?
    #TODO: czy przedzialy w ktorych alfa jest stale nie powinny byc konfigurowalne?
    def learn(self, X, epochs=32000):
        for i in range(4):
            print 'alfa =', self.alfa
            print 'r =', self.r
            for e in range(epochs/4):
                for pict in X:
                    win = self.winner(pict)
                    self.update_weights(pict, win)
            self.alfa /= 2
            self.r -= 2
        self.print_network()

    def print_network(self):
        for k in range(self.outputs):
            print
            for j in range(self.height):
                for i in range(self.width):
                    print self.weights[k][j][i]
                print
