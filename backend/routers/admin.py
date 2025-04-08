from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from sqlalchemy.orm import Session
from core.database import get_db  # 修改导入路径
from auth.models import User
from auth.security import get_password_hash

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("", include_in_schema=False)
async def admin_dashboard(request: Request):
    if not request.session.get("authenticated") or request.cookies.get("user_role") != "admin":
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("admin.html", {"request": request})

@router.get("/users", include_in_schema=False)
async def user_management(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()
    return templates.TemplateResponse("user_mgmt.html", {
        "request": request,
        "users": users
    })

# 添加知识库管理路由
@router.get("/knowledge", include_in_schema=False)
async def knowledge_management(request: Request):
    if not request.session.get("authenticated"):
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("knowledge_upload.html", {"request": request})

@router.get("/get-content")
async def get_content(request: Request, type: str):
    template_map = {
        "users": "user_mgmt.html",
        "knowledge": "knowledge_upload.html",
        "settings": "system_settings.html"
    }
    return templates.TemplateResponse(template_map[type], {"request": request})


from fastapi import APIRouter, Depends, HTTPException

@router.post("/api/users")
async def create_user(
    username: str,
    password: str,
    role: str = "user",
    db: Session = Depends(get_db)
):
    # 检查用户是否存在
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    # 创建新用户
    new_user = User(
        username=username,
        hashed_password=get_password_hash(password),
        role=role
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "用户创建成功", "user_id": new_user.id}


@router.get("/users/create")
async def user_create(request: Request):
    return templates.TemplateResponse("user_create.html", {"request": request})

@router.post("/users/create")
async def create_user(request: Request):
    # 添加实际的用户创建逻辑
    form_data = await request.form()
    # ...处理表单数据...
    return RedirectResponse("/users", status_code=303)