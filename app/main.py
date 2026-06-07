import sys
import os

sys.path.insert(0, os.getcwd())

from app.db import SessionLocal
from app.db import crud

def main():
    db = SessionLocal()
    
    try:
        print("Книжный магазин\n")

        categories = crud.get_all_categories(db)
        print("Категории:")
        for cat in categories:
            print(f"  - {cat.title}")
        
        print("\nКниги:")
        books = crud.get_all_books(db)
        for book in books:
            print(f"  - {book.title}")
            print(f"    Цена: {book.price} руб.")
            print(f"    Описание: {book.description[:50]}..." if len(book.description) > 50 else f"    Описание: {book.description}")
            print(f"    Категория: {book.category.title}")
            print()
        
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()