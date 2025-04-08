from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from sqlalchemy.orm import Session
from core.database import get_db  # 修改导入路径
from auth.models import User
from auth.security import get_password_hash
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
# 删除重复的导入（第10行）
from starlette.templating import Jinja2Templates  # 保留此处
# 删除下面这行重复的导入 ↓
# from starlette.templating import Jinja2Templates

# 初始化模板引擎（添加这部分）
templates = Jinja2Templates(directory="templates")

# 在文件顶部添加路由前缀声明
router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("", include_in_schema=False)
async def admin_dashboard(request: Request):
    if not request.session.get("authenticated"):
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("admin.html", {"request": request})

# 修改其他路由定义（保持相对路径）
@router.get("/users", include_in_schema=False)  # 完整路径会是 /admin/users
async def user_management(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()  # 直接查询完整模型对象
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

# 添加缺失的路由处理
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