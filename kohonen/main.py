# coding=utf-8
from Kohonen import Kohonen
import sys

if len(sys.argv) < 4:
    print 'usage: python main.py training_file test_file conf_file'
    sys.exit(1)

exec("import "+ sys.argv[3] + " as conf")

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


f = open(sys.argv[2], 'r')
pict = []
for line in f:
    l = line.strip().split()
    l[0] = l[0].strip('&')
    pict.append(map(float, l))
print pict
print k.run(pict)
