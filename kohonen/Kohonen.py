import random

class Kohonen(object):
    def __init__(self, width=3, height=3, outputs=4):
        #TODO: dodac bias!
        #TODO: ewentualnie ustawianie alfa
        self.alfa = 0.06
        self.width = width
        self.height = height
        self.outputs = outputs

    def initialize(self):
        random.seed()
        self.weights = [[[random.random() for i in range(self.width)] for j in range(self.height)] for k in range(self.outputs)]
        self.print_network()

    def step(self, pict, k):
        for j in range(self.height):
            for i in range(self.width):
                self.weights[k][j][i] += self.alfa*(pict[j][i]-self.weights[k][j][i])

    def winner(self, pict):
        max_result = float('-infinity')
        max_result_ind = -1
        for k, w in enumerate(self.weights):
            result = 0.0
            for j in range(self.height):
                for i in range(self.width):
                    result += w[j][i] * pict[j][i]
            if result > max_result:
                max_result = result
                max_result_ind = k
        return max_result_ind
            

    def learn(self, X, epochs=32000):
        for e in range(epochs):
            for pict in X:
                k = self.winner(pict)
                self.step(pict, k)
        self.print_network()

    def print_network(self):
        for k in range(self.outputs):
            print
            for j in range(self.height):
                for i in range(self.width):
                    print self.weights[k][j][i]
                print
