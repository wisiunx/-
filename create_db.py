import os
from dotenv import load_dotenv

load_dotenv()

print("DB_HOST:", os.getenv("DB_HOST"))
print("DB_NAME:", os.getenv("DB_NAME"))

from app.db.db import engine
from app.db import models

print("Creating tables...")
models.Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
