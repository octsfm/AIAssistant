# 修改导入路径
from auth.models import User  # 新模型位置

# 保持其他导入不变
from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from sqlalchemy.orm import Session
from core.database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/login", include_in_schema=False)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# 修改登录处理函数
@router.post("/login")
async def handle_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()
    
    if not user or user.hashed_password != password:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "无效凭证"
        })
    
    # 创建响应对象前设置会话
    request.session.update({
        "authenticated": True,
        "user_role": user.role,
        "user_id": str(user.id)
    })
    
    # 合并响应对象设置
    redirect_url = "/admin" if user.role == "admin" else "/user"
    response = RedirectResponse(url=redirect_url, status_code=303)
    response.set_cookie(key="user_role", value=user.role, httponly=True)
    
    return response

@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    response = RedirectResponse(url="/login")
    response.delete_cookie("admin_session")  # 明确删除会话cookie
    return response

# 添加用户仪表盘路由
@router.get("/user", include_in_schema=False)
async def user_dashboard(request: Request):
    if not request.session.get("authenticated"):
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("user.html", {"request": request})