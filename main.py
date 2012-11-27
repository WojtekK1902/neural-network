import sys
from neuralnetwork.Network import Network
from neuralnetwork.FileFormatException import FileFormatException
from helpers.NetworkCreator import NetworkCreator


if __name__ == '__main__':
    try:
        if len(sys.argv) < 2:
            print "usage: python main.py configuration-file <input-file>"
            sys.exit(1)
        f = open(sys.argv[1],'r')
        line = f.readline().strip().split()
        if len(line) < 2:
            raise FileFormatException(f.tell())
        network = Network()
        network.inputs = int(line[0])
        network.outputs = int(line[len(line)-1])
        network.hidden = map(int, line[1:-1])
        print 'Liczba wejsc:', network.inputs
        print 'Liczba warstw ukrytych:', len(network.hidden)
        print 'Warstwy ukryte:', network.hidden
        print 'Liczba wyjsc:', network.outputs
        l = f.readline().strip()
        if not l:
            raise FileFormatException(f.tell())
        network.epochs = int(l)
        print 'Epochs:', network.epochs
        if network.epochs != 0:
            l = f.readline().strip()
            if not l:
                raise FileFormatException(f.tell())
            network.training_file = l

        nc = NetworkCreator()
        network = nc.create_input_layer(network, f)
        network = nc.create_hidden_layers(network, f)

        l = f.readline().strip()
        if l:
            raise FileFormatExcpetion(f.tell())

        network = nc.create_output_layer(network, f)            
        f.close()

        network.print_network()

        input = []
        print

        if len(sys.argv) < 3:
            for i in range(network.inputs):
                input.append(float(raw_input('Input ' + str(i+1) + ': ')))
        else:
            f = open(sys.argv[2], 'r')
            for line in f:
                l = line.strip().split()
                l[0] = l[0].strip('&')
                input.extend(map(float, l))
            f.close()
            
        print 'input =', input

        if network.epochs != 0:
            network.learn()
            network.print_network()

        output = network.compute(input)

        print 'Odpowiedz sieci: ', ['%.4f' % o for o in output]
        
    except FileFormatException as e:
        print 'Bad file format at position:', e.pos
