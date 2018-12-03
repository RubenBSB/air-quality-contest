from keras.layers import LSTM, Dense
from keras.models import Sequential

model = Sequential()
model.add(LSTM(64, input_shape=(None, 500)))
model.add(Dense(1, activation='relu'))
model.compile(optimizer='adam', loss='mse')



