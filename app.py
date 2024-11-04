from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Wczytaj model i zestaw kolumn cech
model = joblib.load("model.pkl")
feature_columns = joblib.load("feature_columns.pkl")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json  # Pobranie danych z żądania

    # Przekształcenie danych na DataFrame
    df = pd.DataFrame([data['features']])

    # Dopasowanie kolumn do tych, które były podczas treningu modelu
    df = df.reindex(columns=feature_columns, fill_value=0)

    # Dokonaj przewidywania
    prediction = model.predict(df)[0]  # Przewidywanie dla pojedynczego rekordu
    return jsonify({"prediction": prediction})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
