from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.sql import func  # 新增导入
from passlib.context import CryptContext

Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String(255))
    role = Column(String(20), default="user")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    file_type = Column(String(20))
    size = Column(Integer)
    upload_time = Column(DateTime(timezone=True), server_default=func.now())