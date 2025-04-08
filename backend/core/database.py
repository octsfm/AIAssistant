from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin123@localhost:5432/mgnt-db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 如果还没有 get_db 函数，请添加以下内容
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()