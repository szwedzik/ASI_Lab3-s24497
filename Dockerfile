# Dockerfile
FROM python:3.10-slim

# Ustawienie katalogu roboczego
WORKDIR /app

# Skopiowanie wszystkich plików do kontenera
COPY . /app

# Instalacja zależności
RUN pip install --no-cache-dir -r requirements.txt

# Otworzenie portu aplikacji
EXPOSE 5000

# Uruchomienie aplikacji Flask
CMD ["python", "app.py"]
