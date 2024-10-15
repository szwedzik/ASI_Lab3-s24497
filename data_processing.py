import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from sklearn.preprocessing import StandardScaler
import logging

# Skonfiguruj loggera
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def connect_to_gsheets():
    """Łączy się z Google Sheets za pomocą Google API."""
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    logging.info('Połączono z Google Sheets')
    return client

def read_data_from_sheets(client):
    """Odczytuje dane z Google Sheets i konwertuje je do DataFrame."""
    spreadsheet = client.open('data_student_24497')  # Podaj nazwę arkusza
    sheet = spreadsheet.sheet1
    data = sheet.get_all_records()  # Pobiera wszystkie rekordy
    df = pd.DataFrame(data)
    logging.info(f"Odczytano {len(df)} wierszy z Google Sheets")
    return df

def clean_data(df):
    """Czyści dane: usuwa lub uzupełnia braki oraz standaryzuje wartości."""
    logging.info('Rozpoczęto czyszczenie danych')

    # Usuwanie wierszy z więcej niż 2 brakującymi wartościami
    initial_rows = len(df)
    df_clean = df.dropna(thresh=5)
    removed_rows = initial_rows - len(df_clean)
    logging.info(f"Usunięto {removed_rows} wierszy z powodu brakujących wartości")

    # Uzupełnianie braków dla kolumn numerycznych medianą
    numeric_cols = df_clean.select_dtypes(include='number').columns
    df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].median())

    # Uzupełnianie braków dla kolumn nienumerycznych za pomocą trybu (najczęściej występującej wartości)
    non_numeric_cols = df_clean.select_dtypes(exclude='number').columns
    for col in non_numeric_cols:
        df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0])

    logging.info(f"Uzupełniono brakujące wartości")

    # Przekształcanie kolumny 'Średnie Zarobki' na numeryczne wartości, wymuszając NaN na nieprawidłowych wartościach
    df_clean['Średnie Zarobki'] = pd.to_numeric(df_clean['Średnie Zarobki'], errors='coerce')

    # Uzupełnianie braków medianą po konwersji
    df_clean['Średnie Zarobki'].fillna(df_clean['Średnie Zarobki'].median(), inplace=True)

    # Standaryzacja zarobków, jeśli kolumna istnieje
    if 'Średnie Zarobki' in df_clean.columns:
        scaler = StandardScaler()
        df_clean[['Średnie Zarobki']] = scaler.fit_transform(df_clean[['Średnie Zarobki']])
        logging.info("Przeprowadzono standaryzację kolumny 'Średnie Zarobki'")

    return df_clean

def generate_report(df, df_clean):
    """Generuje raport z przetworzonych danych i zapisuje go do pliku report.txt."""
    total_rows = len(df)
    cleaned_rows = len(df_clean)
    removed_rows = total_rows - cleaned_rows

    with open('report.txt', 'w') as f:
        f.write(f"Procent usuniętych wierszy: {removed_rows/total_rows*100:.2f}%\n")
        f.write(f"Procent uzupełnionych danych: {cleaned_rows/total_rows*100:.2f}%\n")

    logging.info("Wygenerowano raport: report.txt")

def save_clean_data_to_sheets(df_clean, client):
    """Zapisuje przetworzone dane do Google Sheets."""
    spreadsheet = client.open('data_student_24497')
    sheet = spreadsheet.sheet1

    # Czyszczenie starej zawartości
    sheet.clear()

    # Zapisywanie nowych danych
    sheet.update([df_clean.columns.values.tolist()] + df_clean.values.tolist())
    logging.info("Zapisano przetworzone dane do Google Sheets :)")

if __name__ == "__main__":
    # Połączenie z Google Sheets
    client = connect_to_gsheets()

    # Odczyt danych
    df = read_data_from_sheets(client)

    # Czyszczenie i standaryzacja danych
    df_clean = clean_data(df)

    # Generowanie raportu
    generate_report(df, df_clean)

    # Zapisanie czystych danych z powrotem do Google Sheets
    save_clean_data_to_sheets(df_clean, client)
