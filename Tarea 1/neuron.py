import numpy as np


class Neuron:
    # activation_fun: activation function for this neuron
    # weights: weights for the input values received by this neuron
    # bias: value of the bias for this neuron
    def __init__(self, activation_fun, weights, bias):
        if self._is_numerical(weights) and self._is_numerical([bias]):
            self.activation_fun = activation_fun
            self.W = np.array(weights)
            self.b = bias

            self.input = None
            self.output = None
            self.delta = None
            self.error = None

    # X: input data to get the output from
    # gets the output given some input data
    def feed(self, X):
        if self._is_numerical(X) and self._compare_lengths(X, self.W):
            self.input = X
            z = np.dot(X, self.W) + self.b
            self.output = z
            return self.activation_fun.apply(z)

    # y: true values desired for the output
    # lr: learning rate
    # is_output: true if this neuron is at the last layer
    # trains this neuron, adjusting error, delta, weights and bias
    def train(self, y, lr, is_output=False):
        if is_output:
            self.recalculate_error_output(y)
        else:
            self.recalculate_error_hidden(y[0], y[1])
        self.recalculate_delta()
        self.recalculate_weights(lr)
        self.recalculate_bias(lr)

    # recalculates delta value of this neuron
    def recalculate_delta(self):
        d = self.error * self.activation_fun.derivative(self.output)
        self.delta = d
    
    # next_weights: next layer weights
    # next_deltas: next layer deltas
    # recalculates the error if the neuron is in a hidden layer
    def recalculate_error_hidden(self, next_weights, next_deltas):
        error = np.dot(next_weights, next_deltas)
        self.error = error

    # y: true values desired for the output
    # recalculates the error if the neuron is in an output layer
    def recalculate_error_output(self, y):
        error = y - self.output
        self.error = error

    # lr: learning rate
    # recalculates the weights of this neuron
    def recalculate_weights(self, lr):
        W = self.W + (lr * self.delta * self.input)
        self.W = W

    # lr: learning rate
    # recalculates the bias of this neuron
    def recalculate_bias(self, lr):
        b = self.b + (lr * self.delta)
        self.b = b

    # checks if an array is composed by numerical values
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
