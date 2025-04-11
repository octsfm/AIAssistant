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
    # 添加完整的三项验证（存在性检查 + 角色验证）
    if not all([
        request.session.get("authenticated"),
        request.session.get("user_role") == "admin",
        request.session.get("user_id")  # 新增用户ID验证
    ]):
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("admin.html", {"request": request})

# 正确做法是在每个路由函数内部添加检查
@router.get("/users", include_in_schema=False)
async def user_management(request: Request, db: Session = Depends(get_db)):
    # 权限检查必须写在函数内部
    if not request.session.get("authenticated") or request.session.get("user_role") != "admin":
        return RedirectResponse(url="/login")
    
    users = db.query(User).order_by(User.created_at.desc()).all()
    return templates.TemplateResponse("user/list.html", {
        "request": request,
        "users": users
    })

# 示例修改知识库管理路由
@router.get("/knowledge", include_in_schema=False)
async def knowledge_management(request: Request):
    # 添加权限检查
    if not request.session.get("authenticated") or request.session.get("user_role") != "admin":
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("knowledge_upload.html", {"request": request})

@router.get("/get-content")
async def get_content(request: Request, type: str, db: Session = Depends(get_db)):
    # 添加权限检查
    if not request.session.get("authenticated") or request.session.get("user_role") != "admin":
        return RedirectResponse(url="/login")
    
    # 在get_content函数中修改模板路径
    template_map = {
        "users": ("user/list.html", {"users": db.query(User).all()}),  # 修改路径
        "knowledge": ("knowledge_upload.html", {}),
        "settings": ("system_settings.html", {})
    }
    print(f"Debug - get_content") 
    template, context = template_map[type]
    context["request"] = request
    return templates.TemplateResponse(template, context)


from fastapi import APIRouter, Depends, HTTPException