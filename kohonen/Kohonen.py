import random

class Kohonen(object):
    def __init__(self, width=3, height=3, outputs=4):
        #TODO: ewentualnie ustawianie alfa
        self.alfa = 0.06
        self.width = width
        self.height = height
        self.outputs = outputs

    def initialize(self):
        random.seed()
        self.weights = [[[random.random() for i in range(self.width)] for j in range(self.height)] for k in range(self.outputs)]
        for k in range(self.outputs):
            print
            for j in range(self.height):
                for i in range(self.width):
                    print self.weights[k][j][i]
                print
