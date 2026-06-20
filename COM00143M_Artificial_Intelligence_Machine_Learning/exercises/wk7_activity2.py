# Neural network exercise

import math
import numpy
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error

df = pd.read_csv('cpu.csv')
assert(len(df['vendor'].unique()) == 30)

# Use one-hot encoding to turn a category into a binary column
df = pd.get_dummies(df, columns=["vendor"])

# 80/20 split for training and testing
df_train, df_test = numpy.split(df, [int(.8*len(df))])

scaler = StandardScaler()
df_train_scaled = scaler.fit_transform(df_train)
df_test_scaled = scaler.transform(df_test)

layer_size = 8
iterations = 500
model = MLPRegressor(
    hidden_layer_sizes=(layer_size,),
    activation='logistic',
    max_iter=iterations,
    random_state=0
)

model.fit(df_train_scaled, df_train[:, -1]) 
print(f"Iterations: {model.n_iter_}")
mse = math.sqrt(mean_squared_error(df_train[:, -1], model.predict(df_train_scaled)))
print(f"Root MSE: {mse}")
mae = mean_absolute_error(df_train[:, -1], model.predict(df_train_scaled))
print(f"Absolute error: {mae}")
