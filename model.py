import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from datetime import datetime, timedelta
import os

# 2 saal ka data fetch karo
end_date = datetime.today().strftime('%Y-%m-%d')
start_date = (datetime.today() - timedelta(days=365*2)).strftime('%Y-%m-%d')

symbol = 'AAPL'  # Change this to any other symbol if you want
data = yf.download(symbol, start=start_date, end=end_date)

if data.empty:
    raise ValueError(f"No data fetched for symbol: {symbol}")

# Only use OHLC
data = data[['Open', 'High', 'Low', 'Close']]

# Normalize data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

# Create sequences
X = []
y = []
for i in range(60, len(scaled_data)):
    X.append(scaled_data[i-60:i])
    y.append(scaled_data[i])

X, y = np.array(X), np.array(y)

# Train-test split
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# Build LSTM
model = Sequential()
model.add(LSTM(64, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(Dropout(0.2))
model.add(LSTM(64))
model.add(Dropout(0.2))
model.add(Dense(4))  # 4 outputs for OHLC

model.compile(optimizer='adam', loss='mean_squared_error')

# Train it
model.fit(X_train, y_train, epochs=20, batch_size=32, validation_split=0.1)

# Save it
os.makedirs('models', exist_ok=True)
model.save('models/stock_lstm_model.h5')

# Evaluate
loss = model.evaluate(X_test, y_test)
print(f"Model test loss: {loss}")
