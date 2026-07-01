import pandas as pd
import numpy as np
import re
import os

print("ЗАГРУЗКА ДАННЫХ")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

df_yandex = pd.read_excel(os.path.join(SCRIPT_DIR, 'reviews_yandex.xlsx'), sheet_name='Sheet1')
df_google = pd.read_excel(os.path.join(SCRIPT_DIR, 'reviews_google.xlsx'), sheet_name='Sheet1')
df_2gis = pd.read_excel(os.path.join(SCRIPT_DIR, 'reviews_2gis.xlsx'), sheet_name='Sheet1')

print(f"Яндекс: {len(df_yandex)} отзывов")
print(f"Google: {len(df_google)} отзывов")
print(f"2ГИС: {len(df_2gis)} отзывов")

df_yandex['source'] = 'Yandex'
df_google['source'] = 'Google'
df_2gis['source'] = '2GIS'

df_all = pd.concat([df_yandex, df_google, df_2gis], ignore_index=True)
print(f"Всего отзывов: {len(df_all)}")

print("ОЧИСТКА ДАННЫХ")

df_all = df_all.dropna(subset=['Текст'])
print(f"После удаления пустых текстов: {len(df_all)} отзывов")

df_all = df_all.drop_duplicates(subset=['Текст', 'Автор'], keep='first')
print(f"После удаления дубликатов: {len(df_all)} отзывов")

def extract_rating(value):
    if pd.isna(value):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        numbers = re.findall(r'\d+', value)
        if numbers:
            return float(numbers[0])
    return None

df_all['Оценка_автора_число'] = df_all['Оценка автора'].apply(extract_rating)

print(f"Преобразовано {df_all['Оценка_автора_число'].notna().sum()} оценок в числовой формат")

print("ПРЕДОБРАБОТКА ТЕКСТА")

def clean_text_simple(text):
    if pd.isna(text):
        return ''
    text = str(text).lower()
    text = re.sub(r'[^а-яё\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

df_all['clean_text'] = df_all['Текст'].apply(clean_text_simple)
print("Очистка завершена!")

print("СОЗДАНИЕ НОВЫХ ПРИЗНАКОВ")

df_all['review_length'] = df_all['Текст'].astype(str).apply(len)

def get_category(text):
    text = str(text).lower()
    if any(w in text for w in ['диван', 'кресл', 'пуф', 'софа']):
        return 'Мягкая мебель'
    elif any(w in text for w in ['шкаф', 'стол', 'комод', 'стенк', 'тумб', 'полк']):
        return 'Корпусная мебель'
    elif 'матрас' in text:
        return 'Матрасы'
    elif 'кухн' in text:
        return 'Кухня'
    else:
        return 'Другое'

df_all['category'] = df_all['Текст'].apply(get_category)

def get_sentiment(text):
    text = str(text).lower()
    positive = ['хорош', 'отличн', 'прекрасн', 'доволен', 'спасибо', 'рекоменд', 'супер', 'классн', 'нравит', 'качествен']
    negative = ['ужасн', 'плох', 'отвратит', 'разочар', 'жалею', 'не совету', 'кошмар', 'брак', 'сломал', 'просёл']
    pos_score = sum(1 for w in positive if w in text)
    neg_score = sum(1 for w in negative if w in text)
    if pos_score > neg_score:
        return 'positive'
    elif neg_score > pos_score:
        return 'negative'
    else:
        return 'neutral'

df_all['sentiment'] = df_all['Текст'].apply(get_sentiment)

def get_issue_type(text):
    text = str(text).lower()
    if any(w in text for w in ['доставк', 'опоздал', 'груб', 'сервис', 'не дозвониться', 'привезл', 'поднял', 'срок', 'ждал']):
        return 'Сервис/Доставка'
    elif any(w in text for w in ['брак', 'сломалс', 'царапин', 'просёлся', 'разваливаетс', 'качеств', 'дефект', 'слома']):
        return 'Качество'
    elif any(w in text for w in ['цвет не тот', 'не как на фото', 'размер', 'описани', 'не соответств']):
        return 'Несоответствие описанию'
    else:
        return 'Другое'

df_all['issue_type'] = df_all['Текст'].apply(get_issue_type)

def get_delivery_speed(text):
    text = str(text).lower()
    fast = ['быстр', 'срок', 'оперативн', 'вовремя', 'точно']
    slow = ['долг', 'месяц', 'ждал', 'задержк', 'просроч', 'не довезл']
    fast_score = sum(1 for w in fast if w in text)
    slow_score = sum(1 for w in slow if w in text)
    if fast_score > slow_score:
        return 'fast'
    elif slow_score > fast_score:
        return 'slow'
    else:
        return 'unknown'

df_all['delivery_speed'] = df_all['Текст'].apply(get_delivery_speed)

print("Все признаки созданы!")

print("СТАТИСТИКА ПО ДАННЫМ")

ratings = df_all['Оценка_автора_число'].dropna()
print(f"\nРаспределение оценок (из {len(ratings)} отзывов):")
print(ratings.value_counts().sort_index())

print(f"\nСтатистика оценок:")
print(f"   Средняя оценка: {ratings.mean():.2f}")
print(f"   Медиана: {ratings.median():.2f}")
print(f"   Минимум: {ratings.min():.0f}")
print(f"   Максимум: {ratings.max():.0f}")

print(f"\nРаспределение тональности:")
print(df_all['sentiment'].value_counts())

print(f"\nРаспределение категорий:")
print(df_all['category'].value_counts())

print(f"\nСредняя длина отзыва: {df_all['review_length'].mean():.1f} символов")
print(f"   Максимальная длина: {df_all['review_length'].max()} символов")

print(f"\nПричины негативных отзывов:")
neg_df = df_all[df_all['sentiment'] == 'negative']
print(neg_df['issue_type'].value_counts())

print(f"\nСкорость доставки:")
print(df_all['delivery_speed'].value_counts())

print("СОХРАНЕНИЕ ДАННЫХ")

df_all.to_csv('reviews_all_cleaned.csv', index=False, encoding='utf-8-sig')
print("Сохранено: reviews_all_cleaned.csv")

df_all[df_all['source'] == 'Yandex'].to_csv('reviews_yandex_cleaned.csv', index=False, encoding='utf-8-sig')
df_all[df_all['source'] == 'Google'].to_csv('reviews_google_cleaned.csv', index=False, encoding='utf-8-sig')
df_all[df_all['source'] == '2GIS'].to_csv('reviews_2gis_cleaned.csv', index=False, encoding='utf-8-sig')

print("Сохранены отдельные файлы по источникам")

print("РАБОТА ЗАВЕРШЕНА!")
print(f"\nИтоговое количество отзывов для анализа: {len(df_all)}")