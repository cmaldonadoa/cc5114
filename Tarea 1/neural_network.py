import numpy as np
import activation_functions as af
import neuron_layer as nl


class NeuralNetwork:
    def __init__(self, n_layers, n_neurons_per_layer, n_in, n_out):
        if self._is_numeric((n_layers)) and self._is_numeric(n_neurons_per_layer) and self._is_numeric((n_in)) and self._is_numeric((n_out)):
            self.n_layers = n_layers
            self.n_neurons_per_layer = n_neurons_per_layer
            self.n_in = n_in
            self.n_out = n_out
            self.n_iter = 10000

            self.weights = self._create_weights()
            self.activation_funs = self._create_activations()
            self.layers = np.empty()
            self.lr = 0.01

    def set_activation_functions(self, funs):
        if self._check_length(funs, self.n_layers - 1):
            self.activation_functions = funs

    def set_learning_rate(self, lr):
        if self._is_numeric((lr)):
            self.lr = lr

    def set_weights(self, weights):
        is_numeric = True
        for row in weights:
            is_numeric = is_numeric and self._is_numeric(row)
        if is_numeric and self._check_length(weights, self.n_layers - 1):
            self.weights = weights

    def feed(self, X):
        if self._check_length(X, self.n_in):
            for layer in self.network:
                X = layer.feed(X)
            return X

    def train(self, X, y):
        for i in range(self.n_iter+1):
            a = self.feed(X)
            cost = self._cost(a, y)
            self._backward_prop(y)
            if(i%100 == 0):
                print('Cost after iteration# {:d}: {:f}'.format(i, cost))

    def build(self):
        if self.activation_funs != None and self.weights != None and self.lr != None:
            for w, fun in zip(self.weights, self.activation_funs):
                layer = nl.NeuronLayer(fun, w)
                self.layers.append(layer)

    def _backwards_prop(self, y):
        for i in range(n_layers):
            j = n_layers - i - 1
            layer = self.layers[j]
            arg = None
            if j == n_layers - 1:
                arg = y
            layer.train(self.layers[j + 1], self.lr, y=arg)

    def _cost(self, y, y_test):
        cost = np.sum((y - y_test) ** 2) / self.n_out
        return cost
                
    def _create_weights(self):
        weights = np.empty()
        for n in self.n_neurons_per_layer:
            W = np.random.randn(n)
            weights = np.append(weights, W)
        self.weights = weights
        
    def _create_activations(self):
        funs = np.empty()
        for n in self.n_neurons_per_layer:
            F = np.empty()
            for i in range(n):
                f = af.Sigmoid()
                F = np.append(F, f)
            funs = np.append(funs, F)
        self.activation_funs = funs

    def _is_numeric(self, array):
        for x in array:
            if not isinstance(x, (int, float)):
                raise Exception("Data is non-numerical")
        return True

    def _validate_length(self, arg1, arg2):
        if len(arg1) != len(arg2):
            raise Exception("Inconsistent data length")
        return True

    def _check_length(self, array, l):
        if len(array) != l:
            raise Exception("Inconsistent data length")
        return True
