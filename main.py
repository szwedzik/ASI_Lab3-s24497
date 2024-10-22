import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV

# Wczytaj dane
df = pd.read_csv("https://vincentarelbundock.github.io/Rdatasets/csv/AER/CollegeDistance.csv")

# Analiza eksploracyjna danych
print(df.describe())
print(df.info())

# Sprawdź brakujące wartości
missing_values = df.isnull().sum()
print("Brakujące wartości:\n", missing_values)

# Usuwanie brakujących wartości
df = df.dropna()

# Analiza korelacji
corr_matrix = df.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title("Macierz korelacji")
plt.savefig('correlation_matrix.png')
plt.close()

# Wizualizacja rozkładów zmiennych numerycznych
for col in df.select_dtypes(include=['float64', 'int64']).columns:
    plt.figure()
    df[col].hist(bins=20)
    plt.title(f'Rozkład zmiennej {col}')
    plt.savefig(f'distribution_{col}.png')
    plt.close()

# Inżynieria cech: One-Hot Encoding dla zmiennych kategorycznych
categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

# Usuwamy kolumnę 'score' z listy zmiennych numerycznych, bo to nasz target
numerical_columns.remove('score')

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_columns),
        ('cat', OneHotEncoder(), categorical_columns)])

# Podział danych na zbiór treningowy i testowy
X = df.drop(columns=['score'])
y = df['score']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Pipeline do przetwarzania danych
pipeline = Pipeline(steps=[('preprocessor', preprocessor)])
X_train_transformed = pipeline.fit_transform(X_train)
X_test_transformed = pipeline.transform(X_test)

# Trenowanie modeli: regresja liniowa i las losowy
models = {
    'Linear Regression': LinearRegression(),
    'Random Forest': RandomForestRegressor(random_state=42)
}

results = {}

for model_name, model in models.items():
    model.fit(X_train_transformed, y_train.values.ravel())
    y_pred = model.predict(X_test_transformed)

    # Ewaluacja
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    results[model_name] = {'MSE': mse, 'R²': r2}

    # Zapis wyników do pliku
    with open(f'evaluation_{model_name.replace(" ", "_")}.txt', 'w') as f:
        f.write(f'MSE: {mse}\nR²: {r2}\n')

    # Wizualizacja prognoz vs rzeczywiste wartości
    plt.figure()
    plt.scatter(y_test, y_pred)
    plt.xlabel('Rzeczywiste wyniki')
    plt.ylabel('Prognozowane wyniki')
    plt.title(f'Prognozy vs Rzeczywiste dla {model_name}')
    plt.savefig(f'predictions_vs_actuals_{model_name.replace(" ", "_")}.png')
    plt.close()

# Optymalizacja modelu lasu losowego (przykład GridSearchCV)
param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [10, 20, None]
}

grid_search = GridSearchCV(RandomForestRegressor(random_state=42), param_grid, cv=5)
grid_search.fit(X_train_transformed, y_train.values.ravel())

# Najlepszy model
best_rf = grid_search.best_estimator_
y_pred_best = best_rf.predict(X_test_transformed)

# Ewaluacja najlepszego modelu
best_mse = mean_squared_error(y_test, y_pred_best)
best_r2 = r2_score(y_test, y_pred_best)

# Zapis wyników optymalizacji
with open('evaluation_best_model.txt', 'w') as f:
    f.write(f'Najlepszy model: Random Forest z GridSearchCV\n')
    f.write(f'MSE: {best_mse}\nR²: {best_r2}\n')
