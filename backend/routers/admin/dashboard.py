from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates  # 新增导入
from core.database import get_db
from auth.models import User

router = APIRouter()  # 保持默认路由定义
templates = Jinja2Templates(directory="templates")  # 现在可以正确初始化

# 修改路径定义
@router.get("/", include_in_schema=False)
async def admin_dashboard(request: Request):
    if not all([
        request.session.get("authenticated"),
        request.session.get("user_role") == "admin",
        request.session.get("user_id")
    ]):
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("admin.html", {"request": request})


@router.get("/get-content")  # 保持与前端请求路径一致
async def get_content(
    request: Request, 
    type: str, 
    db: Session = Depends(get_db)
):
    # 权限检查
    if not request.session.get("authenticated") or request.session.get("user_role") != "admin":
        return RedirectResponse(url="/login")
    
    # 更新路由映射表
    route_map = {
        "users": "/users",
        "knowledge": "/knowledge", 
        "settings": "/settings"
    }
    response = await fetch(route_map[type])
    # 完整模板映射
    template_map = {
        "users": ("user/list.html", {}),
        "knowledge": ("knowledge_upload.html", {}),
        "settings": ("system_settings.html", {})  # 确保模板存在
    }
    
    template, context = template_map[type]
    context["request"] = request
    return templates.TemplateResponse(template, context)