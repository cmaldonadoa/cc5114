import activation_functions as af
import neuron_layer as nl
import numpy as np


class NeuralNetwork:
    # n_layers: number of layers in the network
    # n_neurons_per_layer: array with the number of neurons per layer
    # n_in: number of input values
    # n_out: number of output values
    def __init__(self, n_layers, n_neurons_per_layer, n_in, n_out):
        if self._is_numerical([n_layers]) \
                and self._is_numerical(n_neurons_per_layer) \
                and self._is_numerical([n_in]) \
                and self._is_numerical([n_out]):
            self.n_layers = n_layers
            self.n_neurons_per_layer = n_neurons_per_layer
            self.n_in = n_in
            self.n_out = n_out
            
            self.n_iter = 100
            self.weights =  None
            self.activation_funs = None
            self.layers = []
            self.lr = 0.01
            
            self._create_weights()
            self._create_activations()
            
            self.training_results = []
            self.built = False
            
    # n: number of iterations to be set
    # sets the number of iterations of the training
    def set_iterations(self, n):
        if self._is_numerical([n]) and n >= 0:
            self.n_iter = n

    # funs: "2D matrix" with the activation functions to be set on every neuron
    # sets the activation functions of every neuron
    def set_activation_functions(self, funs):
        if self._compare_lengths(funs, self.n_neurons_per_layer):
            for i in range(len(funs)):
                fun = funs[i]
                n = self.n_neurons_per_layer[i]
                self._check_length(fun, n)
            self.activation_funs = funs

    # lr: learning rate to be set
    # sets the learning rate
    def set_learning_rate(self, lr):
        if self._is_numerical([lr]):
            self.lr = lr

    # weights: "3D matrix" with the weights to be set on every neuron
    # sets the weights of every neuron in the network
    def set_weights(self, weights):
        if self._compare_lengths(weights, self.n_neurons_per_layer):
            for i in range(len(self.n_neurons_per_layer)):
                n = self.n_neurons_per_layer[i]
                w = weights[i]
                for j in range(n):
                    if i == 0:
                        self._check_length(w[j], self.n_in)
                    else:
                        self._check_length(
                            w[j], self.n_neurons_per_layer[i - 1])
                    self._is_numerical(w[j])
            self.weights = weights

    # X: input data to get the output from
    # gets the output for an input data
    def feed(self, X):
        if self._check_length(X, self.n_in):
            for layer in self.layers:
                X = layer.feed(X)
            return X

    # X: input data to get the output from
    # y: true values desired for the output
    # trains the network given an input and output data
    def train(self, X, y):
        for X_row, y_row in zip(X, y):
            print(" -------------------- ")
            results = []
            for i in range(self.n_iter+1):
                a = self.feed(X_row)
                results.append(a)
                cost = self._cost(a, y_row)
                self._backwards_prop(y_row)
                if(i%10 == 0):
                    print('Cost after iteration #{:d}: {:f}'.format(i, cost))
            self.training_results.append(results)

    # creates the layer for the network
    def build(self):
        if not self.built:
            for w, fun in zip(self.weights, self.activation_funs):
                layer = nl.NeuronLayer(fun, w)
                self.layers.append(layer)
            self.layers = np.array(self.layers)
            self.built = True

    # applies backward propagation
    def _backwards_prop(self, y):
        for i in range(self.n_layers):
            j = self.n_layers - i - 1
            layer = self.layers[j]
            if i == 0:
                layer.train(self.lr, y=y)
            else:
                layer.train(self.lr, next_layer=self.layers[j + 1])

    # calculates the cost of the prediction
    def _cost(self, y, y_test):
        cost = np.sum((y - y_test) ** 2) / self.n_out
        return cost
      
    # creates default random weights          
    def _create_weights(self):
        weights = []
        for i in range(len(self.n_neurons_per_layer)):
            n = self.n_neurons_per_layer[i]
            weights_i = []
            for j in range(n):
                if i == 0:
                    W = np.random.uniform(-2, 2, self.n_in)
                    weights_i.append(W)
                else:
                    W = np.random.randn(self.n_neurons_per_layer[i - 1])
                    weights_i.append(W)
            weights_i = np.array(weights_i)
            weights.append(weights_i)
        weights = np.array(weights)
        self.set_weights(weights)
        
    # creates default activation functions
    def _create_activations(self):
        funs = []
        for n in self.n_neurons_per_layer:
            F = []
            for i in range(n):
                f = af.Tanh()
                if i % 2 == 0:
                    f = af.Sigmoid()
                F.append(f)
            F = np.array(F)
            funs.append(F)
        self.activation_funs = np.array(funs)

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
    
    # checks if an array has the desired length
    def _check_length(self, array, l):
        if len(array) != l:
            raise Exception("Inconsistent data length")
        return True