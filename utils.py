import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import yfinance as yf
from datetime import datetime, timedelta

def predict_next_7_days(symbol):
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=365*2)).strftime('%Y-%m-%d')

    df = yf.download(symbol, start=start_date, end=end_date)

    if df.empty:
        raise ValueError("No data found for symbol.")

    data = df[['Open', 'High', 'Low', 'Close']]
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)

    last_60_days = scaled_data[-60:]

    model = load_model('models/stock_lstm_model.h5')

    predictions = []
    for _ in range(7):
        input_data = last_60_days.reshape(1, 60, 4)
        pred_scaled = model.predict(input_data)[0]
        pred = scaler.inverse_transform([pred_scaled])[0]

        predictions.append({
            "open": float(pred[0]),
            "high": float(pred[1]),
            "low": float(pred[2]),
            "close": float(pred[3])
        })

        # Update sequence with the latest prediction (in scaled format)
        last_60_days = np.append(last_60_days, [pred_scaled], axis=0)[-60:]

    return predictions
