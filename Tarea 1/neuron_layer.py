import neuron as n
import numpy as np


class NeuronLayer:
    def __init__(self, activation_funs, weights):
        if self._validate_length(activation_funs, weights):
            self.neurons = []
            for f, W in zip(activation_funs, weights):
                neuron = n.Neuron(f, W, 0)
                self.neurons.append(neuron)
            self.neurons = np.array(self.neurons)

            self.input = None
            self.output = None
            self.delta = None
            self.error = None

    def feed(self, X):
        if self._is_numeric(X):
            self.input = X
            Z = []
            for neuron in self.neurons:
                z = neuron.feed(X)
                Z.append(z)
            Z = np.array(Z)
            self.output = Z
            return Z

    def train(self, lr, next_layer=None, y=np.array([])):
        if len(y) == 0: # hidden layer
            for i in range(len(self.neurons)):
                W = []
                D = []         
                for neuron in next_layer.neurons:
                    W.append(neuron.W[i])
                    D.append(neuron.delta)
                self.neurons[i].train([np.array(W), np.array(D)], lr)
        else: # output layer            
            for neuron, out in zip(self.neurons, y):
                neuron.train(out, lr, is_output=True)

    def recalculate_error_output(self, y):
        for neuron, out in zip(self.neurons, y):
            neuron.recalculate_error_output(out) 

    def recalculate_error_hidden(self, next_layer):
        for i in range(len(self.neurons)):
            W = []
            D = []         
            for neuron in next_layer.neurons:
                W.append(neuron.W[i])
                D.append(neuron.d)                
            self.neurons[i].recalculate_error_hidden(np.array(W), np.array(D))
    def _is_numeric(self, array):
        for x in array:
            if not isinstance(x, (int, float)):
                raise Exception("Data is non-numerical")
        return True

    def _validate_length(self, arg1, arg2):
        if len(arg1) != len(arg2):
            raise Exception("Inconsistent data length")
        return True

