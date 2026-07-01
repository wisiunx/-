
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.db import crud
from app.schemas import CategoryCreate, CategoryUpdate, CategoryResponse

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/", response_model=List[CategoryResponse])
def get_all_categories(db: Session = Depends(get_db)):

    categories = crud.get_all_categories(db)
    return categories

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):

    category = crud.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return category

@router.post("/", response_model=CategoryResponse, status_code=201)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):

    existing = crud.get_category_by_title(db, category.title)
    if existing:
        raise HTTPException(status_code=400, detail="Категория с таким названием уже существует")
    
    return crud.create_category(db, category.title)

@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):

    existing = crud.get_category(db, category_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    
    return crud.update_category(db, category_id, category.title)

@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: int, db: Session = Depends(get_db)):

    category = crud.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    
    crud.delete_category(db, category_id)
    return None
