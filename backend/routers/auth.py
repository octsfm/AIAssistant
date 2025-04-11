# 修改导入路径
from auth.models import User  # 新模型位置

# 顶部导入部分添加text
from sqlalchemy import text

# 保持其他导入不变
from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from sqlalchemy.orm import Session
from core.db_init import get_db  # 需要先在db_init.py中定义get_db
from bcrypt import checkpw
from fastapi import HTTPException, status

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login_action(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    print(f"Debug - login") 
    try:
        result = db.execute(
            text("SELECT * FROM users WHERE username = :username"),
            {"username": username}
        )
        user = result.mappings().first()
        
        if not user or not checkpw(password.encode(), user['password'].encode()):
            return templates.TemplateResponse("login.html", {
                "request": request,
                "error": "用户名或密码错误"
            }, status_code=401)
            
        # 登录成功后设置session并跳转
        request.session["authenticated"] = True
        # 现有代码已设置角色信息
        request.session["user_role"] = user['role']
        # 登录成功后设置session并跳转
        request.session["authenticated"] = True
        request.session["user_role"] = user['role']
        request.session["user_id"] = user['id']  # 新增用户ID存储
        return RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)

    except Exception as e:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": f"登录异常: {str(e)}"
        }, status_code=500)

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