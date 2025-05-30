from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import predict_next_7_days

app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        symbol = data.get('symbol', 'AAPL').upper()

        predictions = predict_next_7_days(symbol)
        return jsonify(predictions)

    except Exception as e:
        return jsonify({"error": f"Error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
