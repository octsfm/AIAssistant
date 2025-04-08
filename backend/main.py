from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from routers import auth, admin

app = FastAPI(title="AI管理助手")

# 修复静态文件路径（根据实际目录结构调整）
app.mount("/static", StaticFiles(directory="D:/工作/AI/AI助手/backend/static"), name="static")

# 必须先配置会话中间件
app.add_middleware(
    SessionMiddleware,
    secret_key="your-32-character-secret-key",  # 替换为实际32位密钥
    session_cookie="admin_session",
    same_site="lax"
)

# 注册路由模块
app.include_router(auth.router)
app.include_router(admin.router, prefix="/admin")