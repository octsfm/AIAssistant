from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates
from core.database import get_db
from auth.models import User
from auth.security import get_password_hash,generate_token
from starlette.responses import Response

router = APIRouter(prefix="/user", tags=["user"])
templates = Jinja2Templates(directory="templates")

def admin_required(request: Request):
    """管理员权限验证依赖项"""
    if not request.session.get("authenticated") or request.session.get("user_role") != "admin":
        raise HTTPException(status_code=403, detail="权限不足")

@router.get("/users", include_in_schema=False)
async def user_list(
    request: Request,
    db: Session = Depends(get_db),
    _: None = Depends(admin_required)
):
    print(f"[user.py][71]user_list") 
    users = db.query(User).order_by(User.created_at.desc()).all()
    print(f"[user.py][73]user_list") 
    return templates.TemplateResponse("user/list.html", {  # 修改路径
        "request": request,
        "users": users
    })
    
@router.get("/users/create", include_in_schema=False)
async def create_user_page(request: Request):
    # 生成CSRF令牌并存入session
    csrf_token = generate_token()  # 需要实现生成token的逻辑
    request.session["csrf_token"] = csrf_token
    
    return templates.TemplateResponse("user/create.html", {
        "request": request,
        "csrf_token": csrf_token
    })