from sklearn import datasets
import numpy as np

iris = datasets.load_iris()
X = iris.data
y = iris.target
X_norm = []

# Normalize X
for x in X:
    x_min = min(x)
    x_max = max(x)
    high = 1
    low = 0
    x_norm = normalize(x, x_min, x_max, high, low)
    X_norm.append(x_norm)
    
X = np.array(X_norm)
del X_norm

# 1-hot encoding
y_encoded = []
for out in y:
    



def normalize(x, x_min, x_max, high, low):
    return ((x - x_min) / (x_max - x_min)) * (high - low) + low