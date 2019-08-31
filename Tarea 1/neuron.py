import numpy as np


class Neuron:
    def __init__(self, activation_fun, weights, bias):
        if self._is_numeric(weights) and self._is_numeric((bias)):
            self.activation_fun = activation_fun
            self.W = np.array(weights)
            self.b = bias

            self.input = None
            self.output = None
            self.delta = None
            self.error = None

    def feed(self, X):
        if self._is_numeric(X) and self._validate_length(X, self.W):
            self.input = X
            z = np.dot(X, self.W) + self.b
            self.output = z
            return self.activation_fun.apply(z)

    def train(self, y, lr, is_output=False):
        if is_output:
            self.recalculate_error_output(y)
        else:
            self.recalculate_error_output(y[0], y[1])
        self.recalculate_delta()
        self.recalculate_weights(lr)
        self.recalculate_bias(lr)

    def recalculate_delta(self):
        d = self.error * self.activation_fun.derivative(self.output)
        self.delta = d

    def recalculate_error_hidden(self, next_weights, next_deltas):
        error = np.dot(next_weights, next_deltas)
        self.error = error

    def recalculate_error_output(self, y):
        error = y - self.output
        self.error = error

    def recalculate_weights(self, lr):
        W = self.W + (lr * self.delta * self.input)
        self.W = W

    def recalculate_bias(self, lr):
        b = self.b + (lr * self.delta)
        self.b = b

    def _is_numeric(self, array):
        for x in array:
            if not isinstance(x, (int, float)):
                raise Exception("Data is non-numerical")
        return True

    def _validate_length(self, arg1, arg2):
        if len(arg1) != len(arg2):
            raise Exception("Inconsistent data length")
        return True
