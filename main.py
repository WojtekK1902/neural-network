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

        if network.epochs != 0:
            network.learn()
            network.print_network()

        inputs = []
        print
        q = False

        if len(sys.argv) < 3:
            while q == False:
                input = []
                for i in range(network.inputs):
                    input.append(float(raw_input('Input ' + str(i+1) + ': ')))
                print 'input =', input
                output = network.compute(input)
                print 'Odpowiedz sieci: ', ['%.4f' % o for o in output]
                network.clear_network()
                print
                print 'Jesli chcesz zakonczyc, nacisnij \'q\', jesli kontynuowac, nacisnij dowolny inny klawisz!'
                key = raw_input('Wybor: ')
                if key == 'q':
                    q = True
        else:
            f = open(sys.argv[2], 'r')
            input = []
            for line in f:
                l = line.strip().split()
                l[0] = l[0].strip('&')
                input.extend(map(float, l))
                if len(input) == network.inputs:
                    inputs.append(input)
                    input = []
            f.close()
            for i in inputs:
                print 'input =', i
                output = network.compute(i)
                print 'Odpowiedz sieci: ', ['%.4f' % o for o in output]
                network.clear_network()
                print
        
    except FileFormatException as e:
        print 'Bad file format at position:', e.pos
