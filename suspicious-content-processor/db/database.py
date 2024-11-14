from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
import config

DATABASE_URL = f"postgresql://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@{config.POSTGRES_HOST}/{config.POSTGRES_DB}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# פונקציה ליצירת הטבלאות
def init_db():
    Base.metadata.create_all(bind=engine)
