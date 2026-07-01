
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db import get_db
from app.db import crud
from app.schemas import BookCreate, BookUpdate, BookResponse

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=List[BookResponse])
def get_all_books(
    category_id: Optional[int] = Query(None, description="Фильтр по категории"),
    db: Session = Depends(get_db)
):

    if category_id:
        books = crud.get_books_by_category(db, category_id)
    else:
        books = crud.get_all_books(db)
    

    result = []
    for book in books:
        book_dict = {
            "id": book.id,
            "title": book.title,
            "description": book.description,
            "price": book.price,
            "url": book.url,
            "category_id": book.category_id,
            "category_title": book.category.title if book.category else None
        }
        result.append(book_dict)
    return result

@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):

    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    
    return {
        "id": book.id,
        "title": book.title,
        "description": book.description,
        "price": book.price,
        "url": book.url,
        "category_id": book.category_id,
        "category_title": book.category.title if book.category else None
    }

@router.post("/", response_model=BookResponse, status_code=201)
def create_book(book: BookCreate, db: Session = Depends(get_db)):

    category = crud.get_category(db, book.category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    
    new_book = crud.create_book(
        db,
        title=book.title,
        description=book.description,
        price=book.price,
        category_id=book.category_id,
        url=book.url or ""
    )
    
    return {
        "id": new_book.id,
        "title": new_book.title,
        "description": new_book.description,
        "price": new_book.price,
        "url": new_book.url,
        "category_id": new_book.category_id,
        "category_title": category.title
    }

@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int,
    book: BookUpdate,
    db: Session = Depends(get_db)
):

    existing = crud.get_book(db, book_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    
    # Если меняется категория, проверяем её существование
    if book.category_id is not None:
        category = crud.get_category(db, book.category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Категория не найдена")
    
    updated = crud.update_book(
        db,
        book_id,
        title=book.title,
        description=book.description,
        price=book.price,
        url=book.url,
        category_id=book.category_id
    )
    
    return {
        "id": updated.id,
        "title": updated.title,
        "description": updated.description,
        "price": updated.price,
        "url": updated.url,
        "category_id": updated.category_id,
        "category_title": updated.category.title if updated.category else None
    }

@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):

    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    
    crud.delete_book(db, book_id)
    return None
