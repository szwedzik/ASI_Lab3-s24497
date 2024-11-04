# Analizator Wyników - Model Predykcyjny w Dockerze

Aplikacja Flask do przewidywania cen nieruchomości na podstawie zestawu danych `California Housing`. Model jest uruchamiany w kontenerze Docker i dostępny na Docker Hub.

## Zawartość Repozytorium

- **`app.py`**: Główna aplikacja Flask do obsługi żądań API.
- **`train_model.py`**: Skrypt do trenowania modelu predykcyjnego i zapisu modelu.
- **`model.pkl`**: Wytrenowany model zapisany przy użyciu `joblib`.
- **`Dockerfile`**: Plik konfiguracji Docker do budowania obrazu kontenera.
- **`requirements.txt`**: Lista zależności dla aplikacji.

---

## Klonowanie Repozytorium

Aby rozpocząć, sklonuj repozytorium:

```bash
git clone https://github.com/szwedzik/ASI_Lab4-s24497.git
cd ASI_Lab4-s24497
```

## Uruchomienie Aplikacji Lokalnie

1. Zainstaluj zależności:

```bash
pip install -r requirements.txt
```

2. Wytrenuj model:

```bash
python train_model.py
```
Model zostanie zapisany jako `model.pkl`.

3. Uruchom aplikację Flask:
```bash
python app.py
```

4. **Testowanie API**: Wysłanie żądania `POST` do API na endpoint `/predict`:
```bash
curl -X POST http://localhost:5000/predict \
     -H "Content-Type: application/json" \
     -d '{"features": {"longitude": -122.23, "latitude": 37.88, "housing_median_age": 41.0, "total_rooms": 880.0, "total_bedrooms": 129.0, "population": 322.0, "households": 126.0, "median_income": 8.3252, "ocean_proximity_INLAND": 0, "ocean_proximity_NEAR OCEAN": 1, "ocean_proximity_NEAR BAY": 0, "ocean_proximity_<1H OCEAN": 0}}'

```

## Uruchomienie Aplikacji z Dockerem

1. Zbuduj obraz Docker:
```bash
docker build -t my-predictor-app .
```

2. Uruchom kontener:
```bash
docker run -p 5000:5000 my-predictor-app
```

3. **Testowanie API**: Wysłanie żądania `POST` do API na endpoint `/predict`:

## Korzystanie z Obrazu z Docker Hub

Obraz aplikacji jest dostępny na Docker Hub. Aby uruchomić kontener bez konieczności budowania obrazu lokalnie:

1. Pobierz obraz:
```bash
docker pull your-docker-username/my-predictor-app:latest
```

2. Uruchom kontener:
```bash
docker run -p 5000:5000 your-docker-username/my-predictor-app:latest
```

3. **Testowanie API**: Wysłanie żądania `POST` do API na endpoint `/predict`:

## GitHub Actions: Automatyczne Budowanie i Publikacja
To repozytorium korzysta z GitHub Actions do automatycznego budowania i publikacji obrazu Docker na Docker Hub. Workflow jest uruchamiany przy każdym pushu do gałęzi `main`.

### Konfiguracja GitHub Actions
W repozytorium GitHub skonfiguruj sekrety:
- `DOCKER_USERNAME`: Twoja nazwa użytkownika Docker Hub.
- `DOCKER_PASSWORD`: Hasło lub token dostępu Docker Hub.

Plik workflow `.github/workflows/docker-publish.yml` zawiera kroki do:
1. **Budowania obrazu Docker** na podstawie Dockerfile.
2. **Testowania API** w kontenerze, aby upewnić się, że działa poprawnie.
3. **Publikacji obrazu na Docker Hub**, jeśli testy zakończą się sukcesem.

## Podsumowanie

Analizator Wyników to aplikacja Flask, która wykorzystuje model predykcyjny wytrenowany na danych `California Housing`, aby przewidywać ceny nieruchomości na podstawie szeregu cech, takich jak lokalizacja, wiek budynku, liczba pokoi i inne czynniki. Aplikacja została zapakowana w kontener Docker, co ułatwia jej wdrożenie i uruchomienie na różnych platformach.

W repozytorium znajdują się instrukcje dotyczące:
- Klonowania repozytorium i lokalnego uruchomienia aplikacji.
- Budowania i uruchamiania aplikacji w kontenerze Docker.
- Testowania API poprzez wysyłanie żądań `POST` do endpointu `/predict`.
- Automatyzacji procesu budowy i publikacji obrazu Docker na Docker Hub przy użyciu GitHub Actions.

Dzięki Dockerowi i GitHub Actions, aplikacja jest łatwa do wdrożenia, a każda zmiana w kodzie może być automatycznie przetestowana i opublikowana na Docker Hub. Ten projekt jest przykładem, jak użyć Python, Flask i Docker do tworzenia aplikacji predykcyjnych, które są gotowe do produkcji.
