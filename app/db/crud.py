from sqlalchemy.orm import Session
from . import models

def get_all_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()

def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_category_by_title(db: Session, title: str):
    return db.query(models.Category).filter(models.Category.title == title).first()

def create_category(db: Session, title: str):
    category = models.Category(title=title)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def get_all_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()

def get_books_by_category(db: Session, category_id: int):
    return db.query(models.Book).filter(models.Book.category_id == category_id).all()

def create_book(db: Session, title: str, description: str, price: float, category_id: int, url: str = ""):
    book = models.Book(
        title=title,
        description=description,
        price=price,
        url=url,
        category_id=category_id
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

# ========== UPDATE и DELETE для Category ==========


# ========== UPDATE и DELETE для Category ==========

def update_category(db: Session, category_id: int, title: str):
    """Обновить категорию"""
    category = get_category(db, category_id)
    if category:
        category.title = title
        db.commit()
        db.refresh(category)
    return category

def delete_category(db: Session, category_id: int):
    """Удалить категорию и все связанные с ней книги"""
    category = get_category(db, category_id)
    if category:
        books = get_books_by_category(db, category_id)
        for book in books:
            db.delete(book)
        db.delete(category)
        db.commit()
    return category

# ========== UPDATE и DELETE для Book ==========

def update_book(db: Session, book_id: int, title: str = None, description: str = None,
                price: float = None, url: str = None, category_id: int = None):
    """Обновить книгу"""
    book = get_book(db, book_id)
    if book:
        if title is not None:
            book.title = title
        if description is not None:
            book.description = description
        if price is not None:
            book.price = price
        if url is not None:
            book.url = url
        if category_id is not None:
            book.category_id = category_id
        db.commit()
        db.refresh(book)
    return book

def delete_book(db: Session, book_id: int):
    """Удалить книгу"""
    book = get_book(db, book_id)
    if book:
        db.delete(book)
        db.commit()
    return book

def get_book(db: Session, book_id: int):
    """Получить книгу по ID"""
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_book(db: Session, book_id: int):
    """Получить книгу по ID"""
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_books_by_category(db: Session, category_id: int):
    """Получить все книги категории"""
    return db.query(models.Book).filter(models.Book.category_id == category_id).all()

def get_all_books(db: Session, skip: int = 0, limit: int = 100):
    """Получить все книги"""
    return db.query(models.Book).offset(skip).limit(limit).all()

def search_books(db: Session, query: str):
    """Поиск книг по названию или описанию"""
    return db.query(models.Book).filter(
        models.Book.title.ilike(f"%{query}%") | models.Book.description.ilike(f"%{query}%")
    ).all()
