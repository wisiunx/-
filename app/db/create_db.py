import sys
import os

sys.path.insert(0, os.getcwd())

from app.db import engine
from app.db import models

print("Creating tables...")
models.Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
