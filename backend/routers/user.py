from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates
from core.database import get_db
from auth.models import User
from auth.security import get_password_hash

router = APIRouter(prefix="/user", tags=["user"])
templates = Jinja2Templates(directory="templates")

def admin_required(request: Request):
    """管理员权限验证依赖项"""
    if not request.session.get("authenticated") or request.session.get("user_role") != "admin":
        raise HTTPException(status_code=403, detail="权限不足")

@router.get("/create", include_in_schema=False)
async def create_user_modal(request: Request):
    return templates.TemplateResponse("user/_create_modal.html", {
        "request": request
    })

@router.get("/create", include_in_schema=False)
async def create_user_page(request: Request):
    return templates.TemplateResponse("user/create.html", {"request": request})

@router.post("/create")
async def create_user(
    request: Request,
    db: Session = Depends(get_db),
    _: None = Depends(admin_required)
):
    form_data = await request.form()
    # 添加CSRF验证
    if form_data.get("csrf_token") != request.session.get("csrf_token"):
        raise HTTPException(status_code=403, detail="Invalid CSRF token")
    username = form_data.get("username")
    password = form_data.get("password")
    role = form_data.get("role", "user")

    if not all([username, password]):
        return templates.TemplateResponse("user/create.html", {
            "request": request,
            "error": "用户名和密码不能为空"
        })

    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        return templates.TemplateResponse("user/create.html", {
            "request": request,
            "error": "用户名已存在"
        })

    new_user = User(
        username=username,
        password=get_password_hash(password),
        role=role if role in ["admin", "user"] else "user"
    )
    
    db.add(new_user)
    db.commit()
    
    return RedirectResponse(url="/user/list", status_code=303)

@router.get("/list", include_in_schema=False)
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