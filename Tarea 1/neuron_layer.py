import neuron as n
import numpy as np


class NeuronLayer:
    # activation_funs: array with the activation functions
    #                  to be set on every neuron
    # weights: "2D matrix" with the weights to be set on every neuron
    def __init__(self, activation_funs, weights):
        if self._compare_lengths(activation_funs, weights):
            self.neurons = []
            for f, W in zip(activation_funs, weights):
                neuron = n.Neuron(f, W, 0)
                self.neurons.append(neuron)
            self.neurons = np.array(self.neurons)

            self.input = None
            self.output = None
            self.delta = None
            self.error = None

    # X: input data to get the output from
    # gets the output of every neuron given some input data
    def feed(self, X):
        if self._is_numerical(X):
            self.input = X
            Z = []
            for neuron in self.neurons:
                z = neuron.feed(X)
                Z.append(z)
            Z = np.array(Z)
            self.output = Z
            return Z

    # lr: learning rate
    # next_layer: array with next layer weights and deltas
    # y: true values desired for the output
    # trains every neuron of this layer
    def train(self, lr, next_layer=None, y=np.array([])):
        if len(y) == 0:  # hidden layer
            for i in range(len(self.neurons)):
                W = []
                D = []
                for neuron in next_layer.neurons:
                    W.append(neuron.W[i])
                    D.append(neuron.delta)
                self.neurons[i].train([np.array(W), np.array(D)], lr)
        else:  # output layer
            for neuron, out in zip(self.neurons, y):
                neuron.train(out, lr, is_output=True)

    # cehcks if an array is composed by numerical values
    def _is_numerical(self, array):
        for x in array:
            if not isinstance(x, (int, float)):
                raise Exception("Data is non-numerical")
        return True
        
    # checks if two arrays have the same length
    def _compare_lengths(self, arg1, arg2):
        if len(arg1) != len(arg2):
            raise Exception("Inconsistent data length")
        return True
