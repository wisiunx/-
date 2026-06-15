
import sys
import os

sys.path.insert(0, os.getcwd())

from app.db import SessionLocal
from app.db import crud

def test_crud():
    db = SessionLocal()
    
    try:
        print("=== ТЕСТИРОВАНИЕ CRUD ОПЕРАЦИЙ ===\n")
        
        # 1. CREATE
        print("1. CREATE - создание категории")
        new_cat = crud.create_category(db, "Тестовая категория")
        print(f"   Создана категория: id={new_cat.id}, title={new_cat.title}")
        
        # 2. READ
        print("\n2. READ - чтение категории")
        found_cat = crud.get_category(db, new_cat.id)
        print(f"   Найдена категория: {found_cat.title}")
        
        # 3. UPDATE
        print("\n3. UPDATE - обновление категории")
        updated_cat = crud.update_category(db, new_cat.id, "Обновленная категория")
        print(f"   Обновлено название: {updated_cat.title}")
        
        # 4. DELETE
        print("\n4. DELETE - удаление категории")
        crud.delete_category(db, new_cat.id)
        check_cat = crud.get_category(db, new_cat.id)
        if check_cat is None:
            print("   ✅ Категория успешно удалена")
        
        # 5. CRUD для книг
        print("\n=== ТЕСТИРОВАНИЕ CRUD ДЛЯ КНИГ ===")
        
        test_cat = crud.create_category(db, "Категория для теста книг")
        print(f"Создана категория: {test_cat.title}")
        
        new_book = crud.create_book(db, "Тестовая книга", "Описание", 999, test_cat.id)
        print(f"Создана книга: {new_book.title}")
        
        found_book = crud.get_book(db, new_book.id)
        print(f"Найдена книга: {found_book.title}")
        
        updated_book = crud.update_book(db, new_book.id, title="Обновленная книга", price=777)
        print(f"Обновлена книга: {updated_book.title}, цена: {updated_book.price}")
        
        crud.delete_book(db, new_book.id)
        crud.delete_category(db, test_cat.id)
        
        print("\n=== ВСЕ CRUD ОПЕРАЦИИ УСПЕШНО ПРОВЕРЕНЫ ===")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_crud()
