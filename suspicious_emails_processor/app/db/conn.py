from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:1234@postgres/email_monitor")
KAFKA_BROKER_URL = os.getenv("KAFKA_BROKER_URL", "localhost:9092")
SUSPICIOUS_EMAILS_TOPIC = "suspicious_emails"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    print('try init')
    Base.metadata.create_all(bind=engine)
