from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from routers import auth, admin, user  # 新增user导入
from core.db_init import init_db  # 添加缺失的导入
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# 添加Session中间件（必须配置secret_key）
app.add_middleware(
    SessionMiddleware,
    secret_key="your-secure-key-123",  # 生产环境应使用环境变量
    session_cookie="admin_session",
    same_site="lax"
)

# 其他中间件和路由注册保持在后
app.include_router(auth.router)
# 修改前
app.include_router(admin.router) 

# 修改后（保持路由前缀一致性）
app.include_router(admin.router, prefix="/admin")

# 在FastAPI实例创建后添加
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
async def startup_event():
    init_db()  # 现在可以正确调用初始化函数
from routers import user  # 确保有这行导入
app.include_router(user.router)  # 确保有这行注册