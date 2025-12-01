# backend/database.py
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# ==============================
# DATABASE CONFIG
# ==============================
BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "files.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ==============================
# FILE RECORD MODEL
# ==============================
class FileRecord(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    decrypted_filename = Column(String, nullable=True)
    status = Column(String, nullable=False, default="uploaded")
    created_at = Column(DateTime, default=datetime.utcnow)

# ==============================
# INIT DB FUNCTION
# ==============================
def init_db():
    Base.metadata.create_all(bind=engine)
