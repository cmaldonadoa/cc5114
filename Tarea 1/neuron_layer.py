import neuron as n
import numpy as np


class NeuronLayer:
    def __init__(self, activation_funs, weights):
        if self._validate_length(activation_funs, weights):
            self.neurons = np.empty()
            for f, W in zip(activation_funs, weights):
                neuron = n.Neuron(f, W, 0)
                self.neurons = np.append(self.neurons, neuron)

            self.input = None
            self.output = None
            self.delta = None
            self.error = None

    def feed(self, X):
        if self._is_numeric(X):
            self.input = X
            Z = np.empty()
            for neuron in self.neurons:
                z = neuron.feed(X)
                Z = np.append(Z, z)
            self.output = Z
            return Z

    def train(self, next_layer, lr, y=None):
        if y == None: # hidden layer
            for i in range(len(self.neurons)):
                W = np.empty()
                D = np.empty()         
                for neuron in next_layer.neurons:
                    W = np.append(neuron.W[i])
                    D = np.append(neuron.d)
                self.neurons[i].train((W, D), lr)
        else: # output layer            
            for neuron, out in zip(self.neurons, y):
                neuron.train(out, lr, is_output=True)

    def recalculate_error_output(self, y):
        for neuron, out in zip(self.neurons, y):
            neuron.recalculate_error_output(out) 

    def recalculate_error_hidden(self, next_layer):
        for i in range(len(self.neurons)):
            W = np.empty()
            D = np.empty()         
            for neuron in next_layer.neurons:
                W = np.append(neuron.W[i])
                D = np.append(neuron.d)                
            self.neurons[i].recalculate_error_hidden(W, D)
    def _is_numeric(self, array):
        for x in array:
            if not isinstance(x, (int, float)):
                raise Exception("Data is non-numerical")
        return True
