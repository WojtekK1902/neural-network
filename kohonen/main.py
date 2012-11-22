# coding=utf-8
from Kohonen import Kohonen
import sys

if len(sys.argv) < 3:
    print 'Zbyt mało argumentów'
    sys.exit(1)

exec("from kohonen import "+ sys.argv[2] + " as conf")

k = Kohonen(conf)

k.initialize()
f = open(sys.argv[1], 'r')
#TODO: przeniesc czytanie wektora wejsciowego do Kohonen?
X, w = [], []
for line in f:
    l = line.strip().split()
    if len(l[0].split('&')) == 1:
        if len(w) > 0:
            X.append(w)
        w = []
    l[0] = l[0].strip('&')
    w.append(map(float, l))
X.append(w)

print X
f.close()
k.learn(X)
