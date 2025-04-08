from sqlalchemy import create_engine, MetaData, text, inspect, Column, String, DateTime  # 添加 DateTime
from sqlalchemy.orm import sessionmaker
from bcrypt import hashpw, gensalt
import os
from sqlalchemy import Table, Column, String

# 根据环境变量判断是否在Docker中运行
db_host = "mgmt-db" if os.getenv('IN_DOCKER') else "localhost"

engine = create_engine(
    f"postgresql://postgres:admin123@{db_host}:5432/mgnt-db",
    pool_pre_ping=True
)

# 修复SessionLocal定义
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 移除原有的 session = Session() 定义
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 创建用户表（需补充完整模型）
metadata = MetaData()
metadata.reflect(engine)
# 修改SQL执行部分
# 在文件末尾添加初始化函数
def init_db():
    inspector = inspect(engine)
    if 'users' not in inspector.get_table_names():
        Table('users', metadata,
            Column('username', String(50), primary_key=True),
            Column('password', String(100)),
            Column('role', String(20)),
            Column('created_at', DateTime)  # 现在可以正确识别 DateTime
        )
        metadata.create_all(engine)
    
    # 初始化账户（包含admin和user）
    with SessionLocal() as session:
        # 定义默认账户列表
        default_users = [
            {
                "username": "admin",
                "password": "admin123",
                "role": "admin"
            },
            {
                "username": "user",
                "password": "user123",
                "role": "user"
            }
        ]
        
        # 批量检查并创建用户
        for user_data in default_users:
            if not session.execute(
                text("SELECT 1 FROM users WHERE username = :username"),
                {"username": user_data["username"]}
            ).scalar():
                hashed_pw = hashpw(user_data["password"].encode(), gensalt()).decode()
                session.execute(
                    text("""
                        INSERT INTO users (username, password, role)
                        VALUES (:username, :password, :role)
                    """),
                    {
                        "username": user_data["username"],
                        "password": hashed_pw,
                        "role": user_data["role"]
                    }
                )
        session.commit()