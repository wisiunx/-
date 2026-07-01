
from fastapi import FastAPI
from app.api import categories, books
from app.db import engine, Base

app = FastAPI(
    title="Book API",
    description="API для управления книгами и категориями",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(categories.router)
app.include_router(books.router)

@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в Book API!"}

@app.get("/health")
def health_check():
    """Проверка, что сервис жив"""
    return {"status": "ok", "message": "Book API is running"}

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    print("База данных инициализирована")
