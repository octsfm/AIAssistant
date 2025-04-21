from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from sqlalchemy.orm import Session
from core.database import get_db  # 修改导入路径
from auth.models import User
from auth.security import get_password_hash
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates  # 保留此处


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


# 示例修改知识库管理路由
@router.get("/knowledge", include_in_schema=False)
async def knowledge_management(request: Request):
    # 添加权限检查
    if not request.session.get("authenticated") or request.session.get("user_role") != "admin":
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("knowledge_upload.html", {"request": request})
