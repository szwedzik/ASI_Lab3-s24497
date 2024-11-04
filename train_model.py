import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import joblib

# URL do pobrania zestawu danych California Housing
url = "https://github.com/ageron/handson-ml/raw/master/datasets/housing/housing.csv"

# Wczytaj dane z URL
df = pd.read_csv(url)

# Zakodowanie zmiennej kategorycznej `ocean_proximity` na zmienne numeryczne
df = pd.get_dummies(df, columns=["ocean_proximity"], drop_first=True)

# Usunięcie brakujących wartości
df = df.dropna()

# Przygotowanie danych
X = df.drop(columns=["median_house_value"])
y = df["median_house_value"]

# Zapisz nazwy kolumn (cechy) używane podczas trenowania
feature_columns = X.columns.tolist()
with open("feature_columns.pkl", "wb") as f:
    joblib.dump(feature_columns, f)

# Podział na zbiór treningowy i testowy
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Stworzenie i trening modelu
model = LinearRegression()
model.fit(X_train, y_train)

# Ocena modelu
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# Zapisz model do pliku model.pkl
joblib.dump(model, "model.pkl")
print("Model zapisany jako model.pkl")
