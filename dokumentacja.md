# Raport z analizy danych i budowy modelu predykcyjnego

## 1. Cel projektu
Celem projektu jest zbudowanie modelu predykcyjnego, który przewiduje wartość zmiennej `score` na podstawie dostarczonego zestawu danych. Proces ten obejmuje:
- Eksplorację i wstępną analizę danych,
- Inżynierię cech i przygotowanie danych,
- Wybór i trenowanie modelu,
- Ewaluację oraz optymalizację modelu.

## 2. Eksploracja i wstępna analiza danych

### 2.1. Wczytanie i zapoznanie się z danymi
Dane zostały wczytane z pliku `CollegeDistance.csv`, a wstępne statystyki opisowe ukazują rozkład i właściwości zmiennych.

- **Statystyki opisowe**: 
    - Średnia, mediana, minimum, maksimum i odchylenie standardowe dla zmiennych numerycznych.

### 2.2. Brakujące wartości
Nie wykryto brakujących wartości w żadnej z kolumn, co umożliwia bezpośrednie przystąpienie do dalszych kroków bez imputacji braków.

### 2.3. Analiza korelacji
Obliczono macierz korelacji tylko dla zmiennych numerycznych, aby sprawdzić wzajemne zależności między nimi. Wyniki zostały zapisane jako `correlation_matrix.png`.

## 3. Inżynieria cech i przygotowanie danych

### 3.1. Przetwarzanie zmiennych kategorycznych i numerycznych
- Zmienne kategoryczne zostały zakodowane za pomocą `OneHotEncoder`.
- Zmienne numeryczne zostały standaryzowane przy użyciu `StandardScaler`.

### 3.2. Podział danych
Dane zostały podzielone na zbiór treningowy (80%) i testowy (20%) w sposób losowy, z ustawieniem `random_state=42` dla powtarzalności wyników.

## 4. Wybór i trenowanie modeli

### 4.1. Wybrane modele
Do budowy modelu wybrano:
- **Regresję liniową** - prosty model do wykrywania liniowych zależności.
- **Las losowy** - model bardziej złożony, zdolny do uchwycenia nieliniowych zależności.

### 4.2. Trenowanie modeli
Każdy z modeli został wytrenowany na zbiorze treningowym, a ich prognozy przetestowano na zbiorze testowym.

## 5. Ewaluacja i optymalizacja modelu

### 5.1. Metryki oceny
Modele oceniono przy użyciu następujących metryk:
- **MSE (Mean Squared Error)** - średni błąd kwadratowy
- **R² (R-squared)** - współczynnik determinacji

Wyniki dla każdego modelu zapisano w plikach `evaluation_Linear_Regression.txt` i `evaluation_Random_Forest.txt`. Wykresy porównujące rzeczywiste i prognozowane wartości zapisano jako `predictions_vs_actuals_{model_name}.png`.

### 5.2. Optymalizacja hiperparametrów
Dla modelu lasu losowego przeprowadzono optymalizację hiperparametrów za pomocą `GridSearchCV`. Wyniki najlepszego modelu zapisano w pliku `evaluation_best_model.txt`.

## 6. Wyniki i wnioski

### 6.1. Wyniki modelu
Plik `evaluation_best_model.txt` zawiera następujące wyniki najlepszego modelu:
- **MSE**: wartość błędu kwadratowego dla najlepszego modelu,
- **R²**: wartość współczynnika determinacji, która wskazuje, jak dobrze model wyjaśnia zmienność danych.

### 6.2. Wnioski
- Model lasu losowego po optymalizacji hiperparametrów wykazał wyższą wartość R² oraz niższy MSE, co sugeruje, że jest bardziej skuteczny w przewidywaniu zmiennej `score` niż regresja liniowa.
- W przyszłości można by rozważyć użycie bardziej zaawansowanych algorytmów lub dalszą inżynierię cech, aby poprawić jakość predykcji.
