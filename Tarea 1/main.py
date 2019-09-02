import activation_functions as af
import matplotlib.pyplot as plt
import neural_network as nn
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split


# %%

# Some auxiliary functions

def normalize(x, high, low):
    return ((x - min(x)) / (max(x) - min(x))) * (high - low) + low


def fit(y):
    new_y = []
    for value in y:
        if value < 0.5:
            new_y.append(0.0)
        else:
            new_y.append(1.0)
    return np.array(new_y)


# %%

# Load dataset
dataset = np.loadtxt("datasets/wifi_localization.txt")
n_in = len(dataset[0]) - 1
X = dataset[:, 0:n_in]
y = dataset[:, -1]

# X normalization
high = 1
low = 0
for i in range(n_in):
    X[:, i] = np.apply_along_axis(normalize, 0, X[:, i], high, low)

# y 1-hot encoding
classes = list(set(y))
classes_set = {}
for i in range(len(classes)):
    classes_set[classes[i]] = i

y_encoded = []
for clase in y:
    y_encoded.append(classes_set[clase])
y = np.eye(max(y_encoded) + 1)[y_encoded]
del y_encoded

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                    random_state=42)

# %%

# Neural Network parameters
n_out = len(y[0])
n_layers = 4  # 3 hidden layers + output layer
n_neurons_per_layer = [9, 7, 5, n_out]
inputs_per_layer = [n_in, 9, 7, 5]
n_iter = 100

weights = []
functions = []

# Loop for creating random weights between in range (-2, 2), and activation
# functions alternating between sigmoid and tanh
for i in range(n_layers):
    n = n_neurons_per_layer[i]
    ins = inputs_per_layer[i]
    layer_w = []
    layer_f = []
    for j in range(n):
        layer_w.append(np.random.uniform(-2, 2, ins))
        if i % 2 == 0:
            layer_f.append(af.Sigmoid())
        else:
            layer_f.append(af.Tanh())

    functions.append(np.array(layer_f))
    weights.append(np.array(layer_w))

weights = np.array(weights)
functions = np.array(functions)

#%%

network = nn.NeuralNetwork(n_layers, n_neurons_per_layer, n_in, n_out)

# Set network parameters
network.set_iterations(n_iter)
network.set_learning_rate(0.01)
network.set_weights(weights)
network.set_activation_functions(functions)

# Create layers
network.build()

# Start training
network.train(X_train, y_train)

# %%

# Class predictions
y_predicted = []
for i in range(len(X_test)):
    x_test = X_test[i]
    y_real = y_test[i]
    y_pred = network.feed(x_test)
    y_pred = fit(y_pred)
    y_predicted.append(y_pred)

y_predicted = np.array(y_predicted)

# Confusion matrix
confusion_matrix(y_test.argmax(axis=1), y_predicted.argmax(axis=1))

# %%

# Get results for every epoch of every input
results = network.training_results
fit_results = []

for result in results:
    fit_result = [fit(epoch).argmax() for epoch in result]
    fit_results.append(np.array(fit_result))

fit_results = np.array(fit_results)

# Count correct and incorrect predictions per epoch
corrects = []
incorrects = []
total = len(X_train)
for i in range(len(fit_results[0])):
    epoch_pred = fit_results[:, i]

    correct = 0
    incorrect = 0
    for j in range(len(epoch_pred)):
        correct += int(y_train.argmax(axis=1)[j] == epoch_pred[j])
        incorrect += int(y_train.argmax(axis=1)[j] != epoch_pred[j])

    corrects.append(correct * 1.0 / total)
    incorrects.append(incorrect * 1.0 / total)

# Plot corrects and incorrects percentages per epoch
x_axis_values = [int(i) for i in range(n_iter + 1)]
plt.plot(x_axis_values, corrects, 'b', label='corrects')
plt.plot(x_axis_values, incorrects, 'r', label='incorrects')
plt.xlabel("Number of epoch")
plt.ylabel("Percentage")
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

