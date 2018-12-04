from keras.layers import LSTM, Dense
from keras.models import Sequential
from data.data_preprocess import df_bretagne_horaire_pm10
import numpy as np
import matplotlib.pyplot as plt

%matplotlib inline
plt.rcParams['figure.figsize'] = (10, 6)

model = Sequential()
model.add(LSTM(5, input_shape = (30,1)))
model.add(Dense(1, activation='linear'))
model.compile(optimizer='adam', loss='mse')

df_bretagne_horaire_pm10

val = df_bretagne_horaire_pm10['Brest Mace'].values
m = min(val)
M = max(val)
val2 = (val-m)/(M-m)

def create_dataset(values, look_back):
    X = []
    Y = []
    for k in range(len(values)-look_back+1):
        x = values[k:k+look_back]
        if k+look_back != len(values):
            y = values[k+look_back]
        else:
            y = -1
        X.append(x)
        Y.append(y)
    X = np.array(X)
    Y = np.array(Y)
    return X,Y

X,Y = create_dataset(val2,30)

X = X.reshape(X.shape[0], X.shape[1], 1)


