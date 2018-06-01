import tensorflow as tf
import numpy as np


data = np.loadtxt('final_data.txt', delimiter=',', dtype=np.float32)
x_data = data[:, 0:-1]
y_data = data[:, [-1]]

print(x_data)
print(y_data)