import pandas as pd
import os

print("=" * 50)
print("КОНВЕРТАЦИЯ CSV → EXCEL")
print("=" * 50)

# Список файлов для конвертации
files = [
    'reviews_all_cleaned.csv',
    'reviews_yandex_cleaned.csv',
    'reviews_google_cleaned.csv',
    'reviews_2gis_cleaned.csv'
]

for file in files:
    if os.path.exists(file):
        # Загружаем CSV
        df = pd.read_csv(file, encoding='utf-8-sig')
        
        # Создаем имя для Excel-файла
        excel_name = file.replace('.csv', '.xlsx')
        
        # Сохраняем в Excel
        df.to_excel(excel_name, index=False, engine='openpyxl')
        
        print(f"✅ {file} → {excel_name} ({len(df)} строк)")
    else:
        print(f"⚠️ Файл {file} не найден")

print("\n" + "=" * 50)
print("✅ КОНВЕРТАЦИЯ ЗАВЕРШЕНА!")
print("=" * 50)