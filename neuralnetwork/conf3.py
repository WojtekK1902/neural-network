#Kohonen parameters
output_width = 3
output_height = 3
alfas = [(500, 0.06), (1000, 0.03), (1500, 0.015), (2000, 0.0075), (999999, 0.0)]
r = 1
beta = 0.1
neighbourhood = True
conscience = True

#Grossberg parameters
learning_rates = [(2000, 0.0), (12000, 0.15)]
learning_rule = 'WidrowHoff'

#Backpropagation parameters
bp_learning_rates = [(10000, 0.9), (999999, 0.0)]
