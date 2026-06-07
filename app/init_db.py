
import sys
import os

sys.path.insert(0, os.getcwd())

from app.db import SessionLocal
from app.db import crud
from app.db import models

def init_db():
    db = SessionLocal()
    
    try:
        # Создаём таблицы
        models.Base.metadata.create_all(bind=db.get_bind())
        
        # Добавляем категории
        categories = [
            "Художественная литература",
            "Научно-популярные книги",
            "Программирование"
        ]
        
        for cat_title in categories:
            existing = crud.get_category_by_title(db, cat_title)
            if not existing:
                crud.create_category(db, cat_title)
                print(f"Добавлена категория: {cat_title}")
        
        # Получаем ID категорий
        cat_lit = crud.get_category_by_title(db, "Художественная литература")
        cat_sci = crud.get_category_by_title(db, "Научно-популярные книги")
        cat_prog = crud.get_category_by_title(db, "Программирование")
        
        # Добавляем книги
        books = [
            (cat_lit.id, "Мастер и Маргарита", "Роман Михаила Булгакова", 450),
            (cat_lit.id, "Преступление и наказание", "Роман Фёдора Достоевского", 380),
            (cat_sci.id, "Краткая история времени", "Стивен Хокинг о космологии", 520),
            (cat_sci.id, "Sapiens", "Юваль Ной Харари", 590),
            (cat_prog.id, "Изучаем Python", "Марк Лутц", 1200),
            (cat_prog.id, "Clean Code", "Роберт Мартин", 850),
        ]
        
        for cat_id, title, desc, price in books:
            existing_books = crud.get_books_by_category(db, cat_id)
            if not any(b.title == title for b in existing_books):
                crud.create_book(db, title, desc, price, cat_id)
                print(f"Добавлена книга: {title}")
        
        print("\nБаза данных инициализирована!")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
