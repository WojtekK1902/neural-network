from Kohonen import Kohonen

k = Kohonen()

k.initialize()
f = open('training.data', 'r')
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
